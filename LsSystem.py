# from typing import *

# from LsLines import DirLines, FileLines
# from itertools import chain


# class FSystem:

#     def __init__(self):
#         self._file_lines = FileLines()
#         self._dir_lines = DirLines()

#     def __repr__(self):
#         return '{!r} \n{!r}'.format(self._file_lines, self._dir_lines)

#     def __str__(self):
#         return '\n'.join(chain.from_iterable([self._file_lines.get_lines(), self._dir_lines.get_lines()])

#     @classmethod
#     def _test(cls, line):
#         pass

#     def add(self, e, stats):
#         if e.is_file():
#             self._file_lines.add(e, stats)
#         else:
#             self._dir_lines.add(e, stats)

#     def complete(self):
#         # list_compress = []
#         # for fline in self._lines.get_raw_lines():
#         #     if fline.is_backup:
#         #         if self._lines.mark_backup_line(fline):
#         #             list_compress.append(0)
#         #         else:
#         #             list_compress.append(1)
#         #     else:
#         #         list_compress.append(1)
#         # self._lines.delete_lines(list_compress)
#         self._file_lines.complete()
#         self._dir_lines.complete()

# def _pack_entries(file_lists, dir_lists):
#     dir_lists = list(filter(lambda l: l != [], dir_lists))
#     file_lists = list(filter(lambda l: l != [], file_lists))
#     f_list = list(chain(*file_lists))
#     d_index, d_list = 0, []
#     for i in dir_lists:
#         if len(f_list) > (len(d_list) + len(i)):
#             d_list.extend(i)
#         else:
#             break
#         d_index += 1
#     singles = chain(*dir_lists[d_index:])
#     doubles = zip(f_list, d_list)
#     if len(f_list) != len(d_list):
#         last_singles = islice(f_list, len(d_list), None)
#     else:
#         last_singles = []
#     return singles, doubles, last_singles

# def _generate_narrow(files, dirs):
#     section_seperator = '\n' + '-' * (os.get_terminal_size().columns - 1) + '\n'
#     output = dirs.output()
#     output.extend(files.output())
#     return section_seperator.join(
#         map(lambda x: '\n'.join(x.get_lines()), filter(lambda x: x, output)))

# def _generate_wide(files, dirs):
#     return '\n'.join(
#         list([
#             '{0:<52}|{1}'.format(*l) for l in zip_longest(
#                 chain.from_iterable(
#                     map(lambda x: x.get_lines(), files.output())),
#                 chain.from_iterable(
#                     map(lambda x: x.get_lines(), dirs.output())),
#                 fillvalue=' ')
#         ]))

# def generate_text(files, dirs):
#     return '\n'.join([str(l) for l in [dirs, files]])



    # files, dirs = _get_entries(_path)

    # # generate_text = _generate_wide if os.get_terminal_size(
    # # ).columns > 77 else _generate_narrow
    # print(generate_text(files, dirs))
