from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CompanyForm
from .models import Company


@login_required
def company_setup(request):
    # Agar company already bani hui hai, dobara form mat dikhao
    if hasattr(request.user, "company"):
        return redirect("employer_dashboard")

    # Sirf Employer role wale hi is form ko access kar sakte hain
    if request.user.role != "employer":
        messages.error(request, "Only employers can create a company profile.")
        return redirect("jobseeker_dashboard")

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            messages.success(request, "Company profile created! Waiting for admin approval.")
            return redirect("employer_dashboard")
    else:
        form = CompanyForm()

    return render(request, "companies/company_setup.html", {"form": form})

# Approve and reject code 

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CompanyForm
from .models import Company


def is_admin(user):
    return user.is_authenticated and user.role == "admin"


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def manage_companies(request):
    pending_companies = Company.objects.filter(is_approved=False)
    approved_companies = Company.objects.filter(is_approved=True)
    return render(request, "companies/manage_companies.html", {
        "pending_companies": pending_companies,
        "approved_companies": approved_companies,
    })


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def approve_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.is_approved = True
    company.save()
    messages.success(request, f"{company.company_name} has been approved.")
    return redirect("manage_companies")


@login_required
@user_passes_test(is_admin, login_url="jobseeker_dashboard")
def reject_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.delete()
    messages.success(request, f"{company.company_name} has been rejected and removed.")
    return redirect("manage_companies")

# add logo and location

@login_required
def company_edit(request):
    if not hasattr(request.user, "company"):
        messages.error(request, "You don't have a company profile yet.")
        return redirect("company_setup")

    company = request.user.company

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company profile updated successfully!")
            return redirect("employer_dashboard")
    else:
        form = CompanyForm(instance=company)

    return render(request, "companies/company_edit.html", {"form": form})