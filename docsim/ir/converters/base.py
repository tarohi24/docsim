from pathlib import Path
from typing import Iterable, List

from docsim.ir.models import ColDocument, ColParagraph, QueryDocument


class NoneException(Exception):
    pass


class CannotSplitText(Exception):
    pass


def get_or_raise_exception(obj: Optional[T]) -> T:
    if obj is None:
        raise NoneException
    else:
        return obj


def find_text_or_default(root: ET.Element,
                         xpath: str,
                         default: str) -> str:
    try:
        content: ET.Element = get_or_raise_exception(root.find(xpath))
    except NoneException:
        return default
    try:
        text: str = get_or_raise_exception(content.text)
    except NoneException:
        return default
    return text


class Converter:
    """
    convert something into IRBase
    """
    def _get_docid(self,
                   root: ET.Element) -> str:
        raise NotImplementedError('This is an abstract function')

    def _get_tags(self,
                  root: ET.Element) -> List[str]:
        raise NotImplementedError('This is an abstract function')

    def _get_title(self,
                   root: ET.Element) -> str:
        raise NotImplementedError('This is an abstract function')

    def _get_text(self,
                  root: ET.Element) -> str:
        raise NotImplementedError('This is an abstract function')

    def _get_paragraph_list(self,
                            root: ET.Element) -> List[str]:
        raise NotImplementedError('This is an abstract function')

    def is_valid_text(self,
                      fpath: Path) -> bool:
        """
        Return
        --------------
        True if it is an invalid document (the condition depends on the dataset)
        default: all documents are valid (True)
        """
        return True

    def to_document(self,
                    fpath: Path) -> List[ColDocument]:
        root: ET.Element = ET.parse(str(fpath.resolve())).getroot()

        docid: str = self._get_docid(root)
        tags: List[str] = self._get_tags(root)
        title: str = self._get_title(root)
        text: str = self._get_text(root)
        return [ColDocument(docid=models.KeywordField(docid),
                            title=models.TextField(title),
                            text=models.TextField(text),
                            tags=models.KeywordListField(tags))]

    def to_paragraph(self,
                     fpath: Path) -> List[ColParagraph]:
        root: ET.Element = ET.parse(str(fpath.resolve())).getroot()
        # text
        try:
            paras: List[str] = self._get_paragraph_list(root)
        except Exception as e:
            logger.warning(e, exc_info=True)
            logger.warning('Could not find description field in the original XML.')
        if len(paras) == 0:
            logger.warning('No paragraphs found.')
            return []

        docid: str = self._get_docid(root)
        tags: List[str] = self._get_tags(root)

        return [
            ColParagraph(docid=models.KeywordField(docid),
                         paraid=models.IntField(paraid),
                         text=models.TextField(para),
                         tags=models.KeywordListField(tags))
            for paraid, para in enumerate(paras)]

    def to_query_dump(self,
                      fpath: Path) -> List[QueryDocument]:
        root: ET.Element = ET.parse(str(fpath.resolve())).getroot()

        try:
            paras: List[str] = self._get_paragraph_list(root)
        except Exception as e:
            logger.warning(e, exc_info=True)
            return []
        if len(paras) == 0:
            logger.warning('No paragraphs found.')
            return []

        docid: str = self._get_docid(root)
        tags: List[str] = self._get_tags(root)

        return [
            QueryDocument(docid=docid,
                          paras=paras,
                          tags=tags)]
