from dataclasses import dataclass


@dataclass
class NTCIRConverter(Converter):
    def _get_docid(self,
                   root: ET.Element) -> str:
        pass

    def _get_tags(self,
                  root: ET.Element) -> List[str]:
        pass

    def _get_title(self,
                   root: ET.Element) -> str:

    def _get_text(self,
                  root: ET.Element) -> str:
