from django.shortcuts import render
from django.http import HttpResponse
import stripe
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from priority.models import Clients


""" aqui he cambiado Product por Priority que es lo que la gente esta comprando en el mi app, 
quantity is refer to priority-level, more quantity more level"""

def index(request):
    return HttpResponse("Hello, world. I am in the checkout")


stripe.api_key = settings.STRIPE_SECRET


@login_required()
def checkout(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                priority = get_object_or_404(Clients, pk=id)
                total += quantity * priority.price
                order_line_item = OrderLineItem(
                    order=order,
                    product=priority,
                    quantity=quantity
                )
                order_line_item.save()

            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.error(request, "You have successfully paid")
                request.session['cart'] = {}
                return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
        clients = Clients.objects.all()
        for client in clients:
            print(client.project)
            print(client.supervisor)

    return render(request, "checkout.html",
                  {'order_form': order_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})
