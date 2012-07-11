import sublime, sublime_plugin

DEFAULT_BUILD_CMD = "exec"
DEFAULT_BUILD_TASK = "build"


class MultiTaskExecCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        cmd = kwargs.get("cmd")
        # if cmd is a dict -> multi target build
        # else run normal build
        if isinstance(cmd, dict):
            # store tasks list
            self.tasks = cmd
            # store ordered tasks names
            self.tasknames = sorted(self.tasks.keys())
            # store all build file fields
            self.mainkwargs = kwargs
            # get default_task from build (and remove it from args)
            deftask = self.mainkwargs.pop("default_task", DEFAULT_BUILD_TASK)
            defitem = 0
            if deftask:
                try:
                    defitem = self.tasknames.index(deftask)
                except ValueError:
                    pass
            self.window.show_quick_panel(self.tasknames, self._quick_panel_callback, 0, defitem)
        else:
            self.window.run_command(DEFAULT_BUILD_CMD, kwargs)

    def _quick_panel_callback(self, index):
        if (index > -1):
            # merge main args with target args
            # target args has upper priority
            task = self.mainkwargs
            task.update(self.tasks[self.tasknames[index]])
            # Check for Windows Overrides and Merge
            if sys.platform.startswith('win32'):
                if task.get("windows") and isinstance(task.get("windows"), dict):
                    task.update(task.get("windows"));
                    task.pop("windows");
            # Check for Linux Overrides and Merge
            elif sys.platform.startswith('linux'):
                if task.get("linux") and isinstance(task.get("linux"), dict):
                    task.update(task.get("linux"));
                    task.pop("linux");
            # Check for OSX Overrides and Merge
            elif sys.platform.startswith('darwin'):
                if task.get("osx") and isinstance(task.get("osx"), dict):
                    task.update(task.get("osx"));
                    task.pop("osx");
            # get target command from target build (and remove it from args)
            # if not defined, use default command
            cmd = task.pop("target", DEFAULT_BUILD_CMD)
            # run build
            self.window.run_command(cmd, task)
