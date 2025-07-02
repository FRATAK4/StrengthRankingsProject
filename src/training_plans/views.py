# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import TrainingPlan, Workout


class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ["name", "description", "is_active", "is_public"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["name", "description", "day"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "day": forms.Select(attrs={"class": "form-control"}),
        }


WorkoutFormSet = inlineformset_factory(
    TrainingPlan,  # Model rodzica
    Workout,  # Model dziecka
    form=WorkoutForm,
    extra=0,  # Ile pustych formularzy pokazać na początku
    can_delete=True,  # Czy można usuwać workout
    min_num=1,  # Minimum jeden workout jest wymagany
    validate_min=True,
)

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TrainingPlan


@login_required
def create_training_plan(request):
    if request.method == "POST":
        training_plan_form = TrainingPlanForm(request.POST)

        if training_plan_form.is_valid():
            training_plan = training_plan_form.save(commit=False)
            training_plan.user = request.user  # Przypisujemy aktualnego użytkownika

            workout_formset = WorkoutFormSet(request.POST, instance=training_plan)

            if workout_formset.is_valid():
                training_plan.save()
                workout_formset.save()

                messages.success(request, "Plan treningowy został utworzony!")
                return redirect("training_plan_detail")
            else:
                # Jeśli formset ma błędy, pokażemy je w template
                messages.error(request, "Sprawdź błędy w formularzach workout.")
        else:
            # Jeśli główny formularz ma błędy
            workout_formset = WorkoutFormSet(request.POST)
            messages.error(request, "Sprawdź błędy w formularzu planu treningowego.")
    else:
        # GET request - pokazujemy puste formularze
        training_plan_form = TrainingPlanForm()
        workout_formset = WorkoutFormSet()

    context = {
        "training_plan_form": training_plan_form,
        "workout_formset": workout_formset,
    }
    return render(request, "training_plans/training_plan_create.html", context)


def detail_plan(request):
    return render(request, "training_plans/training_plans_list.html")


@login_required
def edit_training_plan(request, pk):
    training_plan = get_object_or_404(TrainingPlan, pk=pk, user=request.user)

    if request.method == "POST":
        training_plan_form = TrainingPlanForm(request.POST, instance=training_plan)
        workout_formset = WorkoutFormSet(request.POST, instance=training_plan)

        if training_plan_form.is_valid() and workout_formset.is_valid():
            training_plan_form.save()
            workout_formset.save()
            messages.success(request, "Plan treningowy został zaktualizowany!")
            return redirect("training_plan_detail")
    else:
        training_plan_form = TrainingPlanForm(instance=training_plan)
        workout_formset = WorkoutFormSet(instance=training_plan)

    context = {
        "training_plan_form": training_plan_form,
        "workout_formset": workout_formset,
        "training_plan": training_plan,
        "is_edit": True,
    }
    return render(request, "training_plans/training_plan_create.html", context)
