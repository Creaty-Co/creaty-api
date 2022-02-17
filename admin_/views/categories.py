from admin_.views import BaseAdminView
from tags.models import Category
from tags.views import TagsCategoriesView


class AdminCategoriesView(TagsCategoriesView):
    queryset = Category.objects.prefetch_related('tag_set').all()
    permission_classes = TagsCategoriesView.permission_classes + (
        BaseAdminView.permission_classes
    )
