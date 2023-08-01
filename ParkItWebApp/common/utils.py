from ParkItWebApp.parking_spots.models import ParkingSpot
from ParkItWebApp.reviews.models import Review


def get_common_data(user_profile):
    data = {}
    owned_parking_spots = ParkingSpot.objects.filter(owner=user_profile)
    user_bookings = user_profile.bookings.all()
    total_reviews = Review.objects.filter(parking_spot__in=owned_parking_spots)

    if total_reviews:
        user_rating = round(sum(review.rating for review in total_reviews) / len(total_reviews))
    else:
        user_rating = None

    data['owned_parking_spots'] = owned_parking_spots
    data['total_listings'] = len(owned_parking_spots)
    data['total_bookings'] = len(user_bookings)
    data['total_reviews'] = len(total_reviews)
    data['user_rating'] = user_rating
    data['bookings'] = user_bookings

    return data
