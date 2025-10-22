from django.shortcuts import render
from django.views.generic import (
    TemplateView
)
from .forms import (
    WarehouseForm
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

class Warehouse(TemplateView):
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

        context['form'] = WarehouseForm

        context['menu_sections'] = menu_sections

        return context