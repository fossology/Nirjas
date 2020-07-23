from extractor.main import file_runner

def extract(file):
    return file_runner(file)

__all__ = ['file_runner','extract']