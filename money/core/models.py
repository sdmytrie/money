from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    """generic model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


"""
    ACCOUNT
"""


class BankAccount(Post):
    """BankAccount"""

    name = models.CharField(max_length=255)
    iban = models.CharField(max_length=255, null=True)
    bic = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = "bank_account"
        verbose_name = "Compte bancaire"

    def __str__(self):
        return self.bank + " - " + self.name


"""
    THIRD
"""


class Third(Post):
    """Third"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")

    class Meta:
        db_table = "third"
        verbose_name = "Tiers"
        verbose_name_plural = "Tiers"

    def __str__(self):
        return self.name


"""
    CATEGORY
"""


class Category(Post):
    """Category"""

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="children"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")

    class Meta:
        db_table = "category"
        verbose_name = "Catégorie"

    def __str__(self):
        return self.name


"""
    OPERATION
"""


class Operation(Post):
    """Operation"""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account = models.ForeignKey(
        BankAccount, related_name="operations", on_delete=models.CASCADE
    )
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, default="S")
    comment = models.CharField(max_length=255, null=True)
    periodicity = models.IntegerField(default=0)
    third = models.ForeignKey(Third, on_delete=models.CASCADE, null=True)
    balance = models.FloatField(default=0)

    class Meta:
        db_table = "operation"
        verbose_name = "Opération"
        ordering = ["date"]
