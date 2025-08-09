from rest_framework import serializers
from .models import Product, ProductImage, Review, Category

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id','image')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','slug')

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ('id','product','user','rating','comment','created_at')
        read_only_fields = ('user','created_at')

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id','name','slug','description','price','stock','is_active','categories','images','average_rating','created_at')

    def get_average_rating(self, obj):
        qs = obj.reviews.all()
        if not qs.exists(): return None
        return round(sum(r.rating for r in qs) / qs.count(), 2)
