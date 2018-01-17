import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateView

from .models import Slide

REDIS_CACHE = redis.Redis(host="127.0.0.1", port=6379, db=2)

TOPIC = 'remote-control'


def slide_view(request, slug):
    slide = get_object_or_404(Slide, alias=slug, hide=False)
    context = {
        'slide': slide,
        'event_url': reverse('eventsource', args=(slug,)),
        'control_url': reverse('control', args=(slug,)),
    }
    return render(request, 'slide_tmpl.html', context=context)


def eventsource(request, slug):
    ps = REDIS_CACHE.pubsub()
    ps.subscribe([TOPIC + slug])

    def stream_generator():
        for item in ps.listen():
            if item['type'] == 'message':
                # 发送数据
                yield 'event: date\ndata: %s\n\n' % item['data'].decode('utf-8')
    response = StreamingHttpResponse(stream_generator(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response


class ControlView(LoginRequiredMixin, TemplateView):
    login_url = '/admin/'

    template_name = "slide_control.html"
    allowed_operate = {'prev', 'next'}

    def get_context_data(self, slug=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            slide = Slide.objects.get(alias=slug, hide=False)
        except Slide.DoesNotExist:
            return context

        context.update({
            'title': slide.title,
        })
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponse('hello there')

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, slug, *args, **kwargs):
        operator = self.request.POST.get('operator')
        if operator in self.allowed_operate:
            REDIS_CACHE.publish(TOPIC + slug, operator)
        return HttpResponse('ok')
