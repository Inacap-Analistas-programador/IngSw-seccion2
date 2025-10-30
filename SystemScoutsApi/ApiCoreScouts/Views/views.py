from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.apps import apps
from Serializers import serializers_dict


