
ID_ERR = "the id given not is valid "
class ID_ERROR(Exception):...
class FormatError(Exception):...  
NON_ALLOWED_CHARACTERS =  ["\\", "/", ":", "*", "?", '"', "<", ">", "|","_"]
CHARACTERS_ALLOWED = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z","1", "2", "3", "4", "5", "6", "7", "8", "9","0"," "]
LOADING = ['    .', '.    ', '..   ', '...  ', ' ... ', '  ...', '   ..', '    .']