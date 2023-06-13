import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from lesson_27 import settings
from vacancies.models import Vacancy, Skill
from vacancies.serializers import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer


@method_decorator(csrf_exempt, name='dispatch')
class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     search_text = request.GET.get("text", None)
    #
    #     if search_text:
    #         self.object_list = self.object_list.filter(text=search_text)
    #
    #     self.object_list = self.object_list.order_by("text")
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #
    #     # response = []
    #     #
    #     # for vacancy in self.object_list:
    #     #     response.append({
    #     #         "id": vacancy.id,
    #     #         "text": vacancy.text
    #     #     })
    #
    #     list(map(lambda x: setattr(x, "username", x.user.username if x.user else None), page_obj))
    #
    #     response = {
    #         "items": VacancyListSerializer(page_obj, many=True).data,
    #         "num_pages": paginator.num_pages,
    #         "total": paginator.count
    #     }
    #
    #     return JsonResponse(response, safe=False)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    # def get(self, request, *args, **kwargs):
    #     vacancy = self.get_object()
    #
    #     return JsonResponse(VacancyDetailSerializer(vacancy).data)


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    # def post(self, request, *args, **kwargs):
    #     vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
    #     if vacancy_data.is_valid():
    #         vacancy_data.save()
    #     else:
    #         return JsonResponse(vacancy_data.errors)
    #
    #     # vacancy = Vacancy.objects.create(
    #     #     user_id=vacancy_data["user"],
    #     #     slug=vacancy_data["slug"],
    #     #     text=vacancy_data["text"],
    #     #     status=vacancy_data["status"]
    #     # )
    #
    #     return JsonResponse(vacancy_data.data)


@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ["slug", "text", "status", "skills"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacancy_data = json.loads(request.body)

        self.object.slug = vacancy_data["slug"]
        self.object.text = vacancy_data["text"]
        self.object.status = vacancy_data["status"]

        for skill in vacancy_data["skills"]:
            try:
                skill_obj = Skill.objects.get(name=skill)

            except Skill.DoesNotExist:
                return JsonResponse({"error": "Skill not found"}, status=404)
            self.object.skills.add(skill_obj)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "text": self.object.text,
            "slug": self.object.slug,
            "status": self.object.status,
            "created": self.object.created,
            "user": self.object.user_id,
            "skills": list(self.object.skills.all().values_list("name", flat=True)),
        })


@method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)
