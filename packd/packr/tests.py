from django.test import TestCase
from .models import Item, Pack
from django.contrib.auth.models import User

# Create your tests here.

# Test Ideas
# 1. validate that a user shouldn't see another users items (on their dashboard or when creating a Pack).