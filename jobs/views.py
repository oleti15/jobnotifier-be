from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Job,Subscriber
from .serializers import JobSerializer,SubscriberSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
def job_list_api(request):
    jobs = Job.objects.all().order_by('-posted_at')
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def job_detail_api(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)
    serializer = JobSerializer(job)
    return Response(serializer.data)
class SubscriberCreateView(generics.CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def job_create_api(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # saves the new job to the DB
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobListCreateView(APIView):
    """
    GET  /api/jobs/ — list all jobs
    POST /api/jobs/ — create a new job
    """

    def get(self, request):
        jobs = Job.objects.all().order_by('-posted_at')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # saves new job
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.core.mail import send_mail
from django.conf import settings

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def job_create_api(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        job = serializer.save()

        # Notify matching subscribers
        keyword = job.title.lower()
        location = job.location.lower()

        subscribers = Subscriber.objects.filter(
            keyword__icontains=keyword
        )
        if job.location:
            subscribers = subscribers.filter(location__icontains=location)

        for sub in subscribers:
            send_mail(
                subject=f"New Job Alert: {job.title}",
                message=f"A new job matching your interests has been posted:\n\n{job.title}\n{job.description}\nLocation: {job.location}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[sub.email],
                fail_silently=True,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
