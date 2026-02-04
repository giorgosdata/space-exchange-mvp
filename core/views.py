from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Space, CreditTransaction, ExchangeRequest, UserProfile
from .forms import SpaceForm
from django.http import HttpResponseForbidden
from .models import ExchangeMessage
from django.conf import settings
import stripe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("space_list")

EXCHANGE_CREDIT_COST = 10
stripe.api_key = settings.STRIPE_SECRET_KEY
CREDITS_PER_PURCHASE = 50  # πόσα credits θα παίρνει ο χρήστης ανά αγορά

@login_required
def my_account(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    transactions = request.user.credit_transactions.all().order_by("-created_at")[:20]
    return render(
        request,
        "core/my_account.html",
        {"profile": profile, "transactions": transactions},
    )



def space_list(request):
    spaces = Space.objects.all().order_by("-created_at")
    return render(request, "core/space_list.html", {"spaces": spaces})


def space_detail(request, pk):
    space = get_object_or_404(Space, pk=pk)
    return render(request, "core/space_detail.html", {"space": space})


@login_required
def space_create(request):
    if request.method == "POST":
        form = SpaceForm(request.POST)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            space.save()
            return redirect("space_detail", pk=space.pk)
    else:
        form = SpaceForm()

    return render(request, "core/space_form.html", {"form": form})

@login_required
def send_exchange_request(request, space_id):
    space = get_object_or_404(Space, pk=space_id)

    # Δεν μπορεί ο owner να ζητήσει τον δικό του χώρο
    if space.owner == request.user:
        return HttpResponseForbidden("You cannot request your own space.")

    if request.method == "POST":
        message = request.POST.get("message", "").strip()

        ExchangeRequest.objects.create(
            requester=request.user,
            space=space,
            message=message,
        )
        return redirect("my_requests")

    return render(request, "core/send_request.html", {"space": space})

@login_required
def my_requests(request):
    sent_requests = ExchangeRequest.objects.filter(requester=request.user).order_by("-created_at")
    received_requests = ExchangeRequest.objects.filter(space__owner=request.user).order_by("-created_at")

    return render(
        request,
        "core/my_requests.html",
        {
            "sent_requests": sent_requests,
            "received_requests": received_requests,
        },
    )

@login_required
def accept_request(request, pk):
    ex_req = get_object_or_404(ExchangeRequest, pk=pk)

    # Μόνο ο owner του space μπορεί να αποδεχθεί
    if ex_req.space.owner != request.user:
        return HttpResponseForbidden("Not allowed.")

    if ex_req.status != "pending":
        return redirect("my_requests")

    # Χρεώνουμε credits στον requester
    CreditTransaction.objects.create(
        user=ex_req.requester,
        amount=-EXCHANGE_CREDIT_COST,
        reason=f"Exchange accepted for '{ex_req.space.title}'",
    )

    ex_req.status = "accepted"
    ex_req.save()

    return redirect("my_requests")


@login_required
def reject_request(request, pk):
    ex_req = get_object_or_404(ExchangeRequest, pk=pk)

    if ex_req.space.owner != request.user:
        return HttpResponseForbidden("Not allowed.")

    if ex_req.status == "pending":
        ex_req.status = "rejected"
        ex_req.save()

    return redirect("my_requests")

@login_required
def request_chat(request, pk):
    ex_req = get_object_or_404(ExchangeRequest, pk=pk)

    # Μόνο requester ή owner έχουν πρόσβαση
    if not (ex_req.requester == request.user or ex_req.space.owner == request.user):
        return HttpResponseForbidden("Not allowed.")

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            ExchangeMessage.objects.create(
                request=ex_req,
                sender=request.user,
                text=text
            )
        return redirect("request_chat", pk=pk)

    messages = ex_req.messages.all().order_by("created_at")

    return render(
        request,
        "core/request_chat.html",
        {"req": ex_req, "messages": messages},
    )

@login_required
def billing_page(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(
        request,
        "core/billing.html",
        {
            "profile": profile,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        },
    )


@login_required
def create_checkout_session(request):
    # απλό MVP: ένα fixed product/price στο Stripe
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price": settings.STRIPE_PRICE_ID,
                "quantity": 1,
            }
        ],
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
        customer_email=request.user.email or None,
    )
    return redirect(session.url)


@login_required
def billing_success(request):
    # MVP: εδώ απλώς δίνουμε credits (χωρίς webhook verification)
    CreditTransaction.objects.create(
        user=request.user,
        amount=CREDITS_PER_PURCHASE,
        reason="Stripe payment (test)"
    )
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(
        request,
        "core/billing_success.html",
        {"profile": profile, "added": CREDITS_PER_PURCHASE},
    )


@login_required
def billing_cancel(request):
    return render(request, "core/billing_cancel.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # αυτόματα login μετά το signup
            auth_login(request, user)
            return redirect("space_list")
    else:
        form = UserCreationForm()

    return render(request, "core/signup.html", {"form": form})
