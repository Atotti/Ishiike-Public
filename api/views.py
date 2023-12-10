from django.views.generic import View
from django.http import JsonResponse

from review.models import Vote

class CreateVoteView(View):
    '''
    いいね投票作成処理を行う
    '''
    def post(self, request, *args, **kwargs):
        res = {
            'result': False,
            'message': '処理に失敗しました。'
        }
        # POST値に'review_id'がなければBAD REQUESTとする
        if not 'review_id' in request.POST:
            return JsonResponse(res, status=400)
        
        # コメントIDとIPアドレスの取得
        review_id = request.POST['review_id']
        ip_address = get_client_ip(request)

        # 既にIP登録があればコンフリクト
        if Vote.objects.filter(review_id=review_id, ip_address=ip_address):
            res['message'] = '投票済みです'
            return JsonResponse(res, status=201)
        
        # Voteの保存に成功した場合のみ成功
        if Vote.objects.create_vote(ip_address, review_id):
            res['result'] = True
            res['message'] = 'ポイント追加しました'
            return JsonResponse(res, status=201)      
        else:
            return JsonResponse(res, status=500)

def get_client_ip(request):
    '''
    IPアドレスを取得する
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip