from rest_framework import serializers

from .models import Username

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Username
        fields = ('id','username', 'email', 'phone_number', 'created_at', 'age', 'balance')

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Username
        fields = ('id',  'username', 'email', 
                  'phone_number', 'age', 'balance', 
                  'wallet_address','created_at','from_user'
                  )


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, write_only=True
    )
    class Meta:
        model = Username
        fields = ('id',  'username', 'email', 
                  'phone_number', 'age','created_at','password', 'password2'
                  )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError ({'password2': 'Пароли отличаются'})
        if '+996' not in attrs['phone_number']:      
            raise serializers.ValidationError('Номер телефона должен быть в формате +996XXXXXXXXX')
        return attrs

    def create(self, values):
        user = Username.objects.create(
            username=values['username'], phone_number=values['phone_number'],
            age=values['age'], email=values['email'], 
            )
        user.set_password(values['password'])
        user.save()
        return user