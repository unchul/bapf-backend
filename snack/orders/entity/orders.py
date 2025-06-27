from django.db import models
from account.entity.account import Account
from orders.entity.order_status import OrderStatus


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.account}"

    class Meta:
        db_table = 'orders'
        app_label = 'orders'

    def getId(self):
        return self.id
