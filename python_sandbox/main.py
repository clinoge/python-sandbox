import builtins
import socket

from types import new_class

from .exceptions import InvalidOperation

def make_context_manager(module, name, exception=InvalidOperation):
    new_context_manager = new_class(f"__{name}ContextManager")

    save_name = f"_old_{name}"

    def __raise_exception(self, *args, **kwargs):
        raise exception()

    def __save_fn(self):
        setattr(self, save_name, getattr(module, name))

    def __overwrite_fn(self):
        setattr(module, name, __raise_exception)

    def __restore_fn(self):
        setattr(module, name, getattr(self, save_name))

    def __enter__(self):
        self.__save_fn()
        self.__overwrite_fn()

    def __exit__(self, *args, **kwargs):
        self.__restore_fn()

    setattr(new_context_manager, "__raise_exception", __raise_exception)
    setattr(new_context_manager, "__save_fn", __save_fn)
    setattr(new_context_manager, "__overwrite_fn", __overwrite_fn)
    setattr(new_context_manager, "__restore_fn", __restore_fn)
    setattr(new_context_manager, "__enter__", __enter__)
    setattr(new_context_manager, "__exit__", __exit__)

    return new_context_manager

restrict_open = make_context_manager(builtins, "open")
restrict_print = make_context_manager(builtins, "print")
restrict_socket_create_connection = make_context_manager(
    socket, "create_connection"
)
