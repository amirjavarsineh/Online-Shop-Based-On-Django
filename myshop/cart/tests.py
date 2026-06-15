from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Category, Product


class CartTest(TestCase):
    def setUp(self):
        """داده‌های اولیه برای تست‌ها"""
        self.client = Client()
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            price=29.99,
            available=True
        )
        self.add_url = reverse('cart:cart_add', args=[self.product.id])
        self.detail_url = reverse('cart:cart_detail')

    def test_add_to_cart(self):
        """تست افزودن محصول به سبد خرید"""
        response = self.client.post(self.add_url, {
            'quantity': 3,
            'override': False
        })
        # بعد از افزودن، باید به صفحه سبد خرید هدایت شود (status 302)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.detail_url)

        # بررسی سشن: آیا محصول با تعداد صحیح ذخیره شده؟
        session = self.client.session
        cart_data = session.get('cart', {})
        product_key = str(self.product.id)
        self.assertIn(product_key, cart_data)
        self.assertEqual(cart_data[product_key]['quantity'], 3)
        self.assertEqual(cart_data[product_key]['price'], str(self.product.price))

    def test_cart_detail_view(self):
        """تست صفحه نمایش سبد خرید"""
        # ابتدا محصول را به سبد اضافه می‌کنیم
        self.client.post(self.add_url, {'quantity': 2, 'override': False})

        # سپس صفحه سبد خرید را درخواست می‌دهیم
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        # بررسی اینکه نام محصول در صفحه وجود دارد
        self.assertContains(response, self.product.name)
        # بررسی اینکه قیمت کل (2 * 29.99 = 59.98) در صفحه هست
        self.assertContains(response, '59.98')

    def test_remove_from_cart(self):
        """تست حذف محصول از سبد خرید"""
        # اضافه کردن
        self.client.post(self.add_url, {'quantity': 1, 'override': False})
        session = self.client.session
        self.assertIn(str(self.product.id), session.get('cart', {}))

        # حذف کردن
        remove_url = reverse('cart:cart_remove', args=[self.product.id])
        response = self.client.post(remove_url)
        self.assertRedirects(response, self.detail_url)

        # بررسی سشن: محصول نباید وجود داشته باشد
        session = self.client.session
        cart_data = session.get('cart', {})
        self.assertNotIn(str(self.product.id), cart_data)