from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register('food_data', views.food_dataView)
router.register('food_good', views.food_goodView)
router.register('food_bad', views.food_badView)

urlpatterns = router.urls