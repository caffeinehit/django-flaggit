from django import template
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from flaggit import utils
from flaggit.models import Flag, FlagInstance, REVIEW, CONTENT_APPROVED, \
    CONTENT_REJECTED
from flaggit.signals import flagged, review, rejected, approved


class FlaggingTest(TestCase):
    def setUp(self):
        self.hendrix = User.objects.create(username='hendrix')
        self.lennon = User.objects.create(username='lennon')
        self.hendrix.set_password('guitar')
        self.hendrix.save()
        self.ctype = ContentType.objects.get_for_model(self.hendrix)

        self.url = reverse('flaggit')

    def test_anonymous_flagging(self):
        response = self.client.post(self.url, {
            'content_type': self.ctype.id,
            'object_id': self.lennon.id
        })
        
        self.assertEqual(302, response.status_code)
        
        self.assertEqual(1, Flag.objects.all().count())
        self.assertEqual(self.lennon, Flag.objects.all()[0].content_object)
        self.assertEqual(1, Flag.objects.all()[0].flags.count())
        
    def test_non_dupe_anonymous_flagging(self):
        response = self.client.post(self.url, {
            'content_type': self.ctype.id,
            'object_id': self.lennon.id
        })
        
        self.assertEqual(302, response.status_code)
        
        self.assertEqual(1, Flag.objects.all().count())
        self.assertEqual(self.lennon, Flag.objects.all()[0].content_object)
        self.assertEqual(1, Flag.objects.all()[0].flags.count())
        
        response = self.client.post(self.url, {
            'content_type': self.ctype.id,
            'object_id': self.lennon.id
        })
        
        self.assertEqual(302, response.status_code)
        
        self.assertEqual(1, Flag.objects.all().count())
        self.assertEqual(self.lennon, Flag.objects.all()[0].content_object)
        self.assertEqual(1, Flag.objects.all()[0].flags.count())

    def test_flagging(self):
        self.client.login(username='hendrix', password='guitar')
        
        response = self.client.post(self.url, {
            'content_type': self.ctype.id,
            'object_id': self.lennon.id
        })
        
        self.assertEqual(302, response.status_code)
        
        self.assertEqual(1, Flag.objects.all().count())
        self.assertEqual(self.lennon, Flag.objects.all()[0].content_object)
        self.assertEqual(1, Flag.objects.all()[0].flags.count())
        self.assertEqual(self.hendrix, FlagInstance.objects.all()[0].user)
    
    def test_non_dupe_flagging(self):
        self.client.login(username='hendrix', password='guitar')
        
        response = self.client.post(self.url, {
            'content_type': self.ctype.id,
            'object_id': self.lennon.id
        })
        
        self.assertEqual(302, response.status_code)
        
        self.assertEqual(1, Flag.objects.all().count())
        self.assertEqual(self.lennon, Flag.objects.all()[0].content_object)
        self.assertEqual(1, Flag.objects.all()[0].flags.count())
        self.assertEqual(self.hendrix, FlagInstance.objects.all()[0].user)
        
        response = self.client.post(self.url, {
            'content_type': self.ctype.id,
            'object_id': self.lennon.id
        })
        
        self.assertEqual(302, response.status_code)
        
        self.assertEqual(1, Flag.objects.all().count())
        self.assertEqual(self.lennon, Flag.objects.all()[0].content_object)
        self.assertEqual(1, Flag.objects.all()[0].flags.count())
        self.assertEqual(self.hendrix, FlagInstance.objects.all()[0].user)


    def test_flagging_get(self):
        response = self.client.get(self.url, {
            'content_type': self.ctype.id,
            'object_id': self.lennon.id
        })
        
        self.assertEqual(405, response.status_code)

    def test_flagging_fail(self):
        response = self.client.post(self.url, {
            'content_type': self.ctype.id,
            'object_id': 12345
        })
        
        self.assertEqual(400, response.status_code)

    def test_template_tag(self):
        ctx = template.Context({'obj':self.lennon})
        tpl = template.Template("""{% load flaggit_tags %}{% flag_form obj %}""")

        self.assertTrue(isinstance(tpl.render(ctx), unicode))
        
        tpl = template.Template("""{% load flaggit_tags %}{% flag_form obj "flaggit/form.html" %}""")
        
        self.assertTrue(isinstance(tpl.render(ctx), unicode))


    def test_signals(self):
        Handler = type('Handler', (object,), {
            'inc': lambda self: setattr(self, 'i', getattr(self, 'i') + 1),
            'i': 0
        })
        flagged_handler = Handler()
        review_handler = Handler()
        rejected_handler = Handler()
        approved_handler = Handler()
        
        def handle_flagged(sender, flag, created=False, **kwargs):
            if created:
                flagged_handler.inc()
        
        def handle_review(sender, flag, **kwargs):
            review_handler.inc()
            
        def handle_rejected(sender, flag, **kwargs):
            rejected_handler.inc()
        
        def handle_approved(sender, flag, **kwargs):
            approved_handler.inc()
        
        flagged.connect(handle_flagged)
        review.connect(handle_review)
        rejected.connect(handle_rejected)
        approved.connect(handle_approved)

        utils.flag(self.lennon, user=self.hendrix)
        
        flag = Flag.objects.all()[0]
        
        flag.status = REVIEW
        flag.save()
        flag.status = CONTENT_APPROVED
        flag.save()
        flag.status = CONTENT_REJECTED
        flag.save()
        
        self.assertEqual(1, flagged_handler.i)
        self.assertEqual(1, review_handler.i)
        self.assertEqual(1, rejected_handler.i)
        self.assertEqual(1, approved_handler.i)
