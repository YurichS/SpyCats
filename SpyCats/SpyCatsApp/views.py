from rest_framework.viewsets import ModelViewSet
from .models import SpyCat
from .serializers import SpyCatSerializer
from .models import Mission, Target
from .serializers import MissionSerializer, TargetSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class SpyCatViewSet(ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

class MissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response({"error": "Mission is assigned to a cat and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        cat_id = request.data.get('cat')
        mission.cat_id = cat_id
        mission.save()
        return Response({"status": "Cat assigned successfully."})

    @action(detail=True, methods=['patch'])
    def mark_complete(self, request, pk=None):
        mission = self.get_object()
        if mission.is_completed:
            return Response({"error": "Mission is already completed."}, status=status.HTTP_400_BAD_REQUEST)
        for target in mission.targets.all():
            if not target.is_completed:
                return Response({"error": "Not all targets are completed."}, status=status.HTTP_400_BAD_REQUEST)
        mission.is_completed = True
        mission.save()
        return Response({"status": "Mission marked as completed."})

class TargetViewSet(ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    @action(detail=True, methods=['patch'])
    def update_notes(self, request, pk=None):
        target = self.get_object()
        if target.is_completed or target.mission.is_completed:
            return Response({"error": "Cannot update notes on completed target or mission."}, status=status.HTTP_400_BAD_REQUEST)
        target.notes = request.data.get('notes')
        target.save()
        return Response({"status": "Notes updated successfully."})

    @action(detail=True, methods=['patch'])
    def mark_complete(self, request, pk=None):
        target = self.get_object()
        target.is_completed = True
        target.save()
        return Response({"status": "Target marked as completed."})