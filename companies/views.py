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
            company.owner = request.user
            company.save()
            messages.success(request, "Company profile created! Waiting for admin approval.")
            return redirect("employer_dashboard")
    else:
        form = CompanyForm()

    return render(request, "companies/company_setup.html", {"form": form})