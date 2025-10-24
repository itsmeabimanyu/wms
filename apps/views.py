from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView, UpdateView
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

EDIT_BUTTON = """
    <button type="button" class="nav-link btn btn-link text-secondary disabled">
        <i class="far fa-edit"></i> Edit
    </button>
"""

COPY_BUTTON = """
    <button type="button" class="nav-link btn btn-link text-secondary disabled">
        <i class="far fa-copy"></i> Copy
    </button>
"""
               
class CreateWarehouse(TemplateView):
    template_name = 'pages/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edit_button = EDIT_BUTTON
        copy_button = COPY_BUTTON
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
        context['form'] = WarehouseForm
        search_query = self.request.GET.get('search')
        copy_query = self.request.GET.get('copy')

        # Pilih salah satu query yang tersedia
        query = search_query or copy_query

        if query:
            try:
                obj = Warehouse.objects.get(code=query)
                form = WarehouseForm(instance=obj)
                if search_query:
                    # Jadikan semua field readonly
                    context['disable'] = True

                    for field in form.fields.values():
                        field.widget.attrs['readonly'] = True
                        field.widget.attrs['placeholder'] = ""
                        # Aktifkan tombol edit (menuju halaman update)
                        edit_button = f"""
                            <button type="button"
                                    onclick="window.location.href='{reverse('warehouseupdate', args=[obj.pk])}'"
                                    class="nav-link btn btn-link text-info">
                                <i class="far fa-edit"></i> Edit
                            </button>
                        """
                        copy_button = f"""
                            <button type="button"
                                    onclick="window.location.href='{reverse('warehouseview')}?copy={obj.code}'"
                                    class="nav-link btn btn-link text-info">
                                <i class="far fa-copy"></i> Copy
                            </button>
                        """

                context['form'] = form
            except Warehouse.DoesNotExist:
                context['form'] = WarehouseForm()
                context['error'] = "Data tidak ditemukan."
        else:
            context['form'] = WarehouseForm()

        context['navlink'] = f"""
            {edit_button}
            {copy_button}
        """
        context['navtab'] = f"""
            <a class="nav-link active" data-toggle="tab" href="#tab1">Item Entry</a>
            <a class="nav-link" data-toggle="tab" href="#tab2">Item List</a>
            """
        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'save':
            form = WarehouseForm(request.POST)
            if form.is_valid():
                 form.save()

        return redirect(self.request.META.get('HTTP_REFERER'))
    
class UpdateWarehouse(UpdateView):
    template_name = 'pages/create.html'
    model = Warehouse
    form_class = WarehouseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edit_button = EDIT_BUTTON
        copy_button = COPY_BUTTON
        
        search_query = self.request.GET.get('search')
        copy_query = self.request.GET.get('copy')

        # Pilih salah satu query yang tersedia
        query = search_query or copy_query
        if query:
            try:
                obj = Warehouse.objects.get(code=search_query)
                form = WarehouseForm(instance=obj)
                # Jadikan semua field readonly
                if search_query:
                    # Jadikan semua field readonly
                    context['disable'] = True
                    
                    for field in form.fields.values():
                        field.widget.attrs['readonly'] = True
                        field.widget.attrs['placeholder'] = ""
                        # Aktifkan tombol edit (menuju halaman update)
                        edit_button = f"""
                            <button type="button"
                                    onclick="window.location.href='{reverse('warehouseupdate', args=[obj.pk])}'"
                                    class="nav-link btn btn-link text-info">
                                <i class="far fa-edit"></i> Edit
                            </button>
                        """
                        copy_button = f"""
                            <button type="button"
                                    onclick="window.location.href='{reverse('warehouseview')}?copy={obj.code}'"
                                    class="nav-link btn btn-link text-info">
                                <i class="far fa-copy"></i> Copy
                            </button>
                        """

                context['form'] = form
            except Warehouse.DoesNotExist:
                context['form'] = WarehouseForm()
                context['error'] = "Data tidak ditemukan."

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
        context['navtab'] = f"""
            <a class="nav-link active" data-toggle="tab" href="#tab1">Item Entry</a>
            <a class="nav-link" data-toggle="tab" href="#tab2">Item List</a>
            """
        context['navlink'] = f"""
            {edit_button}
            {copy_button}
        """
        return context
    
    def get_success_url(self):
        # Ambil kode warehouse dari instance yang baru disimpan
        code = self.object.code
        base_url = reverse('warehouseview')
        return f"{base_url}?search={code}"
