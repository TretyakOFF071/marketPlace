from django.contrib.auth.models import User
from django.db import models
from django.db.models import F


class Profile(models.Model):
    """Расширенная модель ползьзователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь' )
    balance = models.FloatField(verbose_name='баланс', default=0)
    purchase_amount = models.FloatField(verbose_name='сумма покупок', default=0)

    status_choices = [
        ('new', 'Новичок'),
        ('adv', 'Продвинутый'),
        ('exp', 'Эксперт')
    ]

    status_flag = models.CharField(choices=status_choices, max_length=3,
                                   default='new', verbose_name='статус')

    def add_balance(self, amount):
        Profile.objects.select_for_update().only('balance')\
        .filter(pk=self.pk).update(balance=F('balance') + amount)

    def sub_balance(self, amount):
        Profile.objects.select_for_update().only('balance')\
        .filter(pk=self.pk).update(balance=F('balance') - amount)


    def update_status(self, amount):
        profile = Profile.objects.get(pk=self.pk)
        profile.purchase_amount += amount
        if 5000 <= profile.purchase_amount <= 10000:
            profile.status_flag = 'adv'
        elif profile.purchase_amount > 10000:
            profile.status_flag = 'exp'
        profile.save()



    class Meta:

        db_table = 'profile'
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return f'{self.user.email}'


class GoodCategory(models.Model):

    name = models.CharField(verbose_name='категория товара', max_length=50,
                            db_index=True)

    class Meta:

        db_table = 'category'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


    def __str__(self):
        return f'{self.name}'

class Shop(models.Model):

    name = models.CharField(max_length=20, db_index=True, verbose_name='название магазина')
    log = models.ImageField(upload_to='shop_logo/', verbose_name='логотип магазина')

    class Meta:
        db_table = 'shop'
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'

    def __str__(self):
        return f'{self.name}'

class Good(models.Model):

    name = models.CharField(max_length=25, db_index=True,
                            verbose_name='название товара')
    category = models.ForeignKey(GoodCategory, on_delete=models.CASCADE,
                                 verbose_name='категория',
                                 null=True)
    price = models.FloatField(verbose_name='цена')
    description = models.TextField(verbose_name='описание товара')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='goods',
                             verbose_name='магазин')
    image = models.ImageField(upload_to='goods/',
                              verbose_name='картинка товара')
    amount = models.PositiveIntegerField(verbose_name='кол-во товара')
    activity_choices = [
        ('a', 'Aктивный'),
        ('i', 'Стоп-лист')
    ]

    activity_flag = models.CharField(choices=activity_choices, max_length=1,
                                     default='i', verbose_name='флаг активности')

    def add_amount(self, num):
        Good.objects.select_for_update().only('amount').\
            filter(pk=self.pk).update(amount=F('amount') + num)

    def sub_amount(self, num):
        Good.objects.select_for_update().only('amount').\
            filter(pk=self.pk).update(amount=F('amount') - num)

    class Meta:

        db_table = 'good'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.name}'


class GoodCart(models.Model):

    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, verbose_name='товар', on_delete=models.CASCADE)
    good_num = models.PositiveIntegerField(default=1, verbose_name='кол-во')
    payment_choices = [
        ('p', 'Оплачен'),
        ('n', 'Не оплачен')
    ]
    payment_flag = models.CharField(choices=payment_choices, max_length=1,
                                    default='n', verbose_name='статус оплаты')

    class Meta:
        db_table = 'good2cart'
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'{self.good.name}'


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='пользователь')

    date = models.DateTimeField(auto_now_add=True, verbose_name='дата заказа')
    cart_good = models.ManyToManyField(GoodCart, verbose_name='товар из корзины')
    amount = models.FloatField(default=0, verbose_name='общая стоимость')

    class Meta:

        db_table = 'order'
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
