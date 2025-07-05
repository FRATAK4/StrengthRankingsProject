from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.views.generic import View, DetailView
from .forms import TrainingPlanForm, WorkoutForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TrainingPlan, Workout
from django.db import transaction
from .models import TrainingPlan, Workout, WorkoutExercise, ExerciseSet
from .forms import (
    TrainingPlanForm,
    WorkoutFormSet,
    WorkoutExerciseFormSet,
    ExerciseSetFormSet,
)


class TrainingPlanCreateView(LoginRequiredMixin, View):
    template_name = "training_plans/training_plan_create.html"
    form_class = TrainingPlanForm

    def get_formset_class(self):
        return inlineformset_factory(
            TrainingPlan,
            Workout,
            form=WorkoutForm,
            extra=0,
            can_delete=True,
            min_num=1,
            validate_min=True,
        )

    def get(self, request):
        training_plan_form = self.form_class()
        WorkoutFormSet = self.get_formset_class()
        workout_formset = WorkoutFormSet()

        context = {
            "training_plan_form": training_plan_form,
            "workout_formset": workout_formset,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        training_plan_form = self.form_class(request.POST)
        WorkoutFormSet = self.get_formset_class()

        if training_plan_form.is_valid():
            training_plan = training_plan_form.save(commit=False)
            training_plan.user = request.user

            workout_formset = WorkoutFormSet(request.POST)

            if workout_formset.is_valid():
                with transaction.atomic():
                    training_plan.save()
                    workout_formset.instance = training_plan
                    workout_formset.save()

                messages.success(request, message="Successfully created training plan!")
                return redirect("training_plan_detail", pk=training_plan.pk)
            else:
                messages.error(request, message="Workout form is not valid!")
        else:
            workout_formset = WorkoutFormSet(request.POST)
            messages.error(request, message="Training plan form is not valid!")

        context = {
            "training_plan_form": training_plan_form,
            "workout_formset": workout_formset,
        }

        return render(request, template_name=self.template_name, context=context)


class TrainingPlanUpdateView(LoginRequiredMixin, View):
    template_name = "training_plans/training_plan_create.html"
    form_class = TrainingPlanForm

    def get_formset_class(self):
        return inlineformset_factory(
            TrainingPlan,
            Workout,
            form=WorkoutForm,
            extra=0,
            can_delete=True,
            min_num=1,
            validate_min=True,
        )

    def get_object(self):
        return get_object_or_404(TrainingPlan, pk=self.kwargs.get("pk"))

    def get(self, request):
        training_plan = self.get_object()
        WorkoutFormSet = self.get_formset_class()

        training_plan_form = self.form_class(instance=training_plan)
        workout_formset = WorkoutFormSet(instance=training_plan)

        context = {
            "training_plan_form": training_plan_form,
            "workout_formset": workout_formset,
            "training_plan": training_plan,
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        training_plan = self.get_object()
        WorkoutFormSet = self.get_formset_class()

        training_plan_form = self.form_class(request.POST, instance=training_plan)

        if training_plan_form.is_valid():
            workout_formset = WorkoutFormSet(request.POST, instance=training_plan)

            if workout_formset.is_valid():
                with transaction.atomic():
                    training_plan.save()
                    workout_formset.save()

                messages.success(request, message="Successfully created training plan!")
                return redirect("training_plan_detail", pk=training_plan.pk)
            else:
                messages.error(request, message="Workout form is not valid!")
        else:
            workout_formset = self.get_formset_class()(
                request.POST, instance=training_plan
            )
            messages.error(request, message="Training plan form is not valid!")

        context = {
            "training_plan_form": training_plan_form,
            "workout_formset": workout_formset,
        }

        return render(request, template_name=self.template_name, context=context)


class TrainingPlanDetailView(DetailView):
    model = TrainingPlan
    template_name = "training_plans/training_plan.html"
    context_object_name = "training_plan"
