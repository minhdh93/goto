import webbrowser
from ..gotomagic.utils import is_file
from ..gotomagic.text import GotoWarning
from .open import open


def default(magic, args, verbose=False):
    """
    Default behaviour when no commands are found in the first argument
    """

    output = ""
    for magicword in args:
        url = magic.get_uri(magicword)
        # for this time beeing, the get_uri is exiting and printing warning itself
        #  TODO:  it would be better to have that kind of logic up in here.
        if url is None:
            return None, GotoWarning('magicword_does_not_exist', magicword=magicword)  # noqa

        if is_file(url):
            _output, err = open(magic, '', [magicword], verbose)
            if err:
                return None, err
            output += "%s\n" % _output
        else:
            try:
                webbrowser.open_new_tab(url)
                output += "%s\n" % url
            except webbrowser.Error:
                return None, GotoError('open_browser_tab_error')

    return output if verbose else None, None
