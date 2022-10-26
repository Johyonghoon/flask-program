from dataclasses import dataclass


@dataclass
class Dataset(object):

    context: str    #파일 저장경로
    fname: str      #파일 이름
    train: object   #train.csv 가 데이터프레임으로 전환된 객체(읽어들여야 할 파일)
    test: object    #test.csv 가 데이터프레임으로 전환된 객체(읽어들여야 할 파일)
    id: str         #탑승자 승선번호(문제)
    label: str      #탑승자 승선번호에 따른 생존여부(정답)

    # 데이터를 읽고(getter = property) / 쓰기(setter) 기능을 추가한다.

    @property
    def context(self) -> str: return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def train(self) -> object: return self._train

    @train.setter
    def train(self, train): self._train = train

    @property
    def test(self) -> object: return self._test

    @test.setter
    def test(self, test): self._test = test

    @property
    def id(self) -> str: return self._id

    @id.setter
    def id(self, id): self._id = id

    @property
    def label(self) -> str: return self._label

    @label.setter
    def label(self, label): self._label = label
