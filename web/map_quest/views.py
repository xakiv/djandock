from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect

from map_quest.forms import DatasetForm
from map_quest.models import Dataset
from map_quest.models import Subset


def index(request):
    datasets = Dataset.objects.all()
    return render(request, 'map_quest/index.html', {'datasets': datasets})


def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    return render(request, 'map_quest/dataset_detail.html', {'dataset': dataset})


def dataset_create(request):
    if request.method != 'POST':
        form = DatasetForm()
        return render(request, 'map_quest/dataset_create.html', {'form': form})


def dataset_delete(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    dataset.delete()
    return redirect('map_quest:index')


def dataset_update(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    if request.method != 'POST':
        form = DatasetForm(instance=dataset)
    else:
        form = DatasetForm(request.POST, instance=dataset)
        if form.is_valid():
            form.save()
    return render(request, 'map_quest/dataset_edit.html', {'form': form})


def subset_list(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    subsets = Subset.objects.filter(dataset=dataset)
    return render(request, 'map_quest/subset_list.html', {'dataset': dataset, 'subsets': subsets})
