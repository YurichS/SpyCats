from rest_framework import serializers
from .models import SpyCat, Target, Mission

class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = '__all__'

class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, required=False)

    class Meta:
        model = Mission
        fields = '__all__'

    def create(self, validated_data):
        targets_data = validated_data.pop('targets', [])
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission
