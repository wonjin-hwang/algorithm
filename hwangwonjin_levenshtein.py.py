import numpy as np
from collections import Counter

# refer = '나는너를좋아해'  # 발성 내용
# hyper = '너는나좋아하니'  # 인식 결과


class Levenshtein(object):

    def __init__(self):
        super(Levenshtein, self).__init__()

    @staticmethod
    def editDistance(refer, hyper):
        #[step1] Levenshtein Distance 구현
        ##클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어##
        """
        [step1] Levenshtein Distance 구현

        :param refer: reference (비교 기준)
        :param hyper: STT result (비교할 텍스트)
        :return: Levenshtein Distance Matrix (len(r) * len(h))
        """
        # 구현
        #나는너를좋아해
        #너는나좋아하니

        distance_matrix = np.zeros((len(refer)+1)*(len(hyper)+1)).reshape(len(refer)+1,len(hyper)+1)
        for i in range(len(refer)+1):
            for j in range(len(hyper)+1):
                if i==0:
                    distance_matrix[0][j]= j
                elif j==0:
                    distance_matrix[i][0] = i

        print(distance_matrix)

                    #로직 짜기
        for i in range(1,len(refer)+1):
            for j in range(1,len(hyper)+1):
                if refer[i-1]==hyper[j-1]:
                    distance_matrix[i][j]=distance_matrix[i-1][j-1]
                else:

                    distance_matrix[i][j]=min(distance_matrix[i-1][j-1],distance_matrix[i-1][j],distance_matrix[i][j-1])+1

        print(distance_matrix)



        print(distance_matrix)

        return distance_matrix

    # [step1] Levenshtein Distance 구현
##클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어####클리어##




    @staticmethod
    def getStepList(refer, hyper, distance_matrix):
        """
        [step2] TOT, MAT, INS, DEL, SUB 리스트 출력 함수

        :param refer: Reference : 발성내용 나는너를좋아해
        :param hyper: STT result :인식 결과 너도나좋아하니
        :param distance_matrix: Levenshtein Distance Matrix : 위에서 만든 행렬
        :return:  Matched info list
        """



        # 구현
        match_list = list()
        x = len(refer)
        y = len(hyper)

        while x > 0 and y > 0:
            if distance_matrix[x][y] == distance_matrix[x - 1][y - 1]:
                print("Match")
                match_list.append("m")
                x -= 1
                y -= 1

            elif distance_matrix[x][y] == distance_matrix[x - 1][y] + 1:
                print("Insert Error")
                match_list.append("i")
                x -= 1

            elif distance_matrix[x][y] == distance_matrix[x][y - 1] + 1:
                print("Delete Error")
                match_list.append("d")
                y -= 1

            elif distance_matrix[x][y] == distance_matrix[x - 1][y - 1] + 1:
                print("Substitute Error")
                match_list.append("s")
                x -= 1
                y -= 1

        # 맨 처음 셀에 도달했을 때 종료합니다.
        print("Reached the beginning of the matrix")

        print(match_list)


        # 두 값을 비교해서 조건을 만족하면 어느쪽으로 간다.
        # 그리고 거기서 똑같은 과정
        # 0.0까지 가면 종료한다.
        return match_list


def cer(info):
    """
    [step3] 음절 인식 결과 정보 리턴 함수

    :param r: Reference
    :param h: STT result
    :param d: Levenshtein Distance Matrix
    :return:  Matched info list
    """
    element_counts = {}

    # 각 요소의 개수를 세기 위해 반복문 사용
    for element in match_list:
        if element in element_counts:
            element_counts[element] += 1
        else:
            element_counts[element] = 1

    num_total = len(refer)
    num_mat = element_counts['m']
    num_ins = element_counts['i']
    num_del = element_counts['d']
    num_sub = element_counts['s']
    cer_rate = (num_total - (num_ins + num_del + num_sub)) / num_total

    r_sent = info.get('ref')
    h_sent = info.get('hyp')

    # 구현
    distance = Levenshtein()
    distance_matrix=distance.editDistance(r_sent,h_sent)
    match_list = distance.getStepList(r_sent,h_sent,distance_matrix)



    # 리턴 예시
    cer_info = {'cer': cer_rate, 'tot': num_total,
                'mat': num_mat, 'sub': num_sub,
                'del': num_del, 'ins': num_ins,
                'list': match_list}
    print(cer_info)
    return cer_info


if __name__ == '__main__':

    refer = '안녕하세요만나서반갑습니다'  # 발성 내용
    hyper = '안녕하세요오만나반갑습니당'  # 인식 결과

    refer = '사랑합니다'     # 발성 내용
    hyper = '서랑함다'      # 인식 결과

    refer = '나는너를좋아해'  # 발성 내용
    hyper = '너는나좋아하니'  # 인식 결과

    sentence_info = {'ref': refer, 'hyp': hyper}
    cer_info = cer(sentence_info)

    print('refer : %s' % refer)
    print('hyper : %s' % hyper)
    print('match list : ', cer_info.get('list'))

    # Edit --------------------------------------
    cer_rate = cer_info.get('cer')
    print('cer : %f' % cer_rate if cer_rate > 0 else 0.0)  # 인식률 (Character Error Rate)
    # -------------------------------------------

    print('tot : %d' % cer_info.get('tot'))  # 전체 음절 수
    print('mat : %d' % cer_info.get('mat'))  # 매치 음절 수
    print('sub : %d' % cer_info.get('sub'))  # 교체 에러 수
    print('ins : %d' % cer_info.get('ins'))  # 삽입 에러 수
    print('del : %d' % cer_info.get('del'))  # 삭제 에러 수
