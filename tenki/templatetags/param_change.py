from django import template

register = template.Library()

#リクエストボディ(パラメータ)の書き換え・追加(pageの番号を指定)、クエリストリングだけ返却
@register.simple_tag()
def url_replace(request, field, value):
    copied           = request.GET.copy()
    copied[field]    = value
    return copied.urlencode()
