from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'subcategory', SubCategoryViewSet,basename='subcategory')
router.register(r'category', CategoryViewSet,basename='category')
router.register(r'generics',GenericViewSet,basename='generics')
router.register(r'profile_setup', AddStudioViewSet, basename='add_studio')
router.register(r'update_studio', UpdateStudioViewSet,basename='update_studio')
router.register(r'edit_studio', EditStudioViewset,basename='edit_studio')
router.register(r'specific_user_category', SpecificStudioViewSet,basename='Specific_Studio_Detail')
router.register(r'nearby_user_category', StudioMapViewset,basename='nearby_user_category_list')
router.register(r'genre_wise_studio', GenreWiseStudioViewSet,basename='category')
router.register(r'reviews', RatingViewSet, basename='Rating')
router.register(r'specific_studio_reviews', SpecificStudioRatingViewSet, basename='Rating')
router.register(r'favourite_studio', FavouriteStudioViewsets, basename='fav_studio')
router.register(r'get_studio', GetSpecificStudioViewSet, basename='GetSpecificStudioViewSet')
router.register(r'raise_dispute', RaiseDisputeViewset, basename='raise_dispute')
router.register(r'check_slots_availability', CheckAvailabilityViewset, basename='check_slots_availability')

urlpatterns = router.urls
