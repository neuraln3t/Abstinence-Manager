from counter.models import *
from django.utils import timezone

Trophy.objects.create(name="The beginning", 
description="Even the choice of starting your journey to becoming abstinent is worth a trophy by itself!",
time_required=timezone.timedelta(seconds=1))

Trophy.objects.create(name="First day", 
description="Congrats, you made it through your first day! Keep it up!",
time_required=timezone.timedelta(days=1))

Trophy.objects.create(name="Three days", 
description="Bravo, you already reached three days! Wasn't too bad, was it?",
time_required=timezone.timedelta(days=3))

Trophy.objects.create(name="One week", 
description="The first week is always the hardest but you did it! We're proud of you!",
time_required=timezone.timedelta(days=7))

Trophy.objects.create(name="Two weeks", 
description="Congratulations, you reached the two week mark!",
time_required=timezone.timedelta(days=14))

Trophy.objects.create(name="One month", 
description="We are very proud of you for making it through an entire month. Well done!",
time_required=timezone.timedelta(days=30))