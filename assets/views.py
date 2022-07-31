from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Asset, Tag
from .forms import AssetForm, ReviewForm
from .utils import searchAssets, paginateAssets


def assets(request):
    assets, search_query = searchAssets(request)
    custom_range, assets = paginateAssets(request, assets, 6)

    context = {'assets': assets,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'assets/assets.html', context)


def asset(request, pk):
    assetObj = Asset.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.asset = assetObj
        review.owner = request.user.profile
        review.save()

        assetObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('asset', pk=assetObj.id)

    return render(request, 'assets/single-asset.html', {'asset': assetObj, 'form': form})


@login_required(login_url="login")
def createAsset(request):
    profile = request.user.profile
    form = AssetForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, "assets/asset_form.html", context)


@login_required(login_url="login")
def updateAsset(request, pk):
    profile = request.user.profile
    asset = profile.asset_set.get(id=pk)
    form = AssetForm(instance=asset)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()

        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            asset = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                asset.tags.add(tag)

            return redirect('account')

    context = {'form': form, 'asset': asset}
    return render(request, "assets/asset_form.html", context)


@login_required(login_url="login")
def deleteAsset(request, pk):
    profile = request.user.profile
    asset = profile.asset_set.get(id=pk)
    if request.method == 'POST':
        asset.delete()
        return redirect('assets')
    context = {'object': asset}
    return render(request, 'delete_template.html', context)
