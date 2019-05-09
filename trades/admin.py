from django.contrib import admin

# Register your models here.
from .models import Trade

# register the Trade class to admin panel
@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):

    # fields displayed in admin panel list view
    list_display = ('ticker', 'name', 'asset_class', 'user', 'currency',
        'number_of_shares', 'action', 'price_paid', 'trade_date', 'total_value')

    fieldsets = [
        ('Trade detail', # label displayed in admin trade detail
        # displayed / editable fields in detail panel :
        {'fields': ['user', 'name', 'asset_class', 'ticker', 'currency', 'number_of_shares', 'action',
        'price_paid', 'trade_date']})
    ]

    # this adds a filter feature on the right of the panel
    list_filter = ['user']

    # this add a search text field
    search_fields = ['ticker']
