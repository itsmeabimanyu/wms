from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView
)
from .forms import (
    WarehouseForm
)

from .models import (
    Warehouse
)

# Create your views here.
class Dashboard(TemplateView):
    template_name = 'layouts/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_sections = [
            {
                "label": "Elements",
                "items": [
                    {"name": "Buttons", "url": "elem-buttons.html"},
                    {"name": "Dropdown", "url": "elem-dropdown.html"},
                    {"name": "Icons", "url": "elem-icons.html"},
                ],
            },
            {
                "label": "Forms",
                "items": [
                    {"name": "Form Elements", "url": "form-elements.html"},
                ],
            },
            {
                "label": "Charts",
                "items": [
                    {"name": "ChartJS", "url": "chart-chartjs.html"},
                ],
            },
            {
                "label": "Tables",
                "items": [
                    {"name": "Basic Tables", "url": "table-basic.html"},
                ],
            },
        ]

        context['menu_sections'] = menu_sections

        return context

class ViewWarehouse(TemplateView):
    template_name = 'pages/summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_sections = [
            {
                "label": "Inventory",
                "items": [
                    {"name": "Warehouse", "url": "warehouseview"},
                ],
            },
        ]

        context['menu_sections'] = menu_sections

        return context
    
class CreateWarehouse(TemplateView):
    template_name = 'pages/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_sections = [
            {
                "label": "Inventory",
                "items": [
                    {"name": "Warehouse", "url": "warehouseview"},
                ],
            },
        ]

        context['menu_sections'] = menu_sections
        context['items'] = Warehouse.objects.all()

        # Ambil keyword dari query string (?search=...)
        search_query = self.request.GET.get('search')
        context['form'] = WarehouseForm
        if search_query:
            try:
                obj = Warehouse.objects.get(code=search_query)  # ganti 'kode' sesuai field kamu
                context['form'] = WarehouseForm(instance=obj)
            except Warehouse.DoesNotExist:
                context['form'] = WarehouseForm()
                context['error'] = "Data tidak ditemukan."
        else:
            context['form'] = WarehouseForm()

        # Query dasar
        queryset = Warehouse.objects.all()

        # Kalau ada input search, filter berdasarkan field tertentu
        """if search_query:
            queryset = queryset.filter(
                Warehouse.Q(code__icontains=search_query) |
                Warehouse.Q(name__icontains=search_query) |
                Warehouse.Q(address__icontains=search_query)
            )"""

        context['search_query'] = search_query  # biar bisa ditampilkan ulang di input search

        context['navlink'] = f"""
            <button type="submit" name="action" value="save" class="nav-link btn btn-link text-info">
                <i class="far fa-save"></i> Save
            </button>
            <button type="submit" name="action" value="edit" class="nav-link btn btn-link disabled">
                <i class="far fa-edit"></i> Edit
            </button>
            <button type="submit" name="action" value="copy" class="nav-link btn btn-link disabled">
                <i class="far fa-copy"></i> Copy
            </button>
            <button type="submit" name="action" value="view" class="nav-link btn btn-link disabled">
                <i class="far fa-copy"></i> View
            </button>
        """
        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'save':
            form = WarehouseForm(request.POST)
            if form.is_valid():
                 form.save()

        return redirect(self.request.META.get('HTTP_REFERER'))
