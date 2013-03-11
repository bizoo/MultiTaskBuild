====================================
Multi task Builder for SublimeText 2
====================================

This plugin adds the ability to define more than one task (target) in a single sublime-build file.

When you run the Build command, a menu ask you which task you want to execute.

**Update variants:**

SublimeText 2 Build 2197 introduce a new option "variants" in sublime-build file.

See `this link
<http://docs.sublimetext.info/en/latest/reference/build_systems.html#variants>`_ for more info.

Like this plugin, you can now have different tasks that is available on the Command Palette prefixed with "Build: ".


How it works
------------

This plugin is designed to be a drop in replacement for the standard *exec* command (the command that is executed by the Build command in ST2).
It means that actual sublime-build files must run exactly the same way as before.

This plugin define a new format for sublime-build file that supports multi target build.

The best way to understand new format is to look at `Example: Multi task Python Builder`_.

In brief:

- **cmd** become a dictionary that contain one entry for each task.
- The fields that could be declared in each task are exactly the same as the standard fields (cmd, file_regex, working_dir, ...)
- The fields declared in the root are the defaults for all tasks. Same fields declared inside the task as upper priority.
- There is a new optional field default_task that define the default task. The default value is 'build'.


Example: Multi task Python Builder
----------------------------------

This is the standard Python sublime-build included with ST2::

	{
		"cmd": ["python", "-u", "$file"],
		"file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
		"selector": "source.python"	
	}


Now this is a multi task Python sublime-build::

    {
    	"cmd": {
    		"build": {
    			"cmd": ["python", "-u", "$file"]			
    		},
    		"verbose": {
    			"cmd": ["python", "-u", "-v", "$file"],
    			"quiet": true
    		}
    	},
    	"file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
    	"selector": "source.python",
    	"default_task": "verbose",
    	"target": "multi_task_exec"
    }


If you compare these files, this exactly the same structure except:

- To use this plugin you have to set **multi_task_exec** in the **target** field.
- **cmd** field become a dictionary that contain one entry for each task. The fields that could be declared in each task are exactly the same as the standard fields (cmd, file_regex, working_dir, ...).
- The optional field **default_task** define the default task. The default value is 'build'.
- **file_regex** is the default for all task. This value is used for each task except for tasks that redeclare **file_regex**.

Known issues
------------

There is actually only one things which can cause problems:

Expandable variables (like '$file', '$file_path', ...) are expanded by ST2 **before** calling the *exec* command.
And not all fields from the sublime-build file are expanded (cmd and working_dir only I think).

So for the variables of tasks to be expanded, I have to put tasks in the **cmd** fields.
The drawback is that **all** fields from tasks are expanded, so if you put a '$file' string in the *path* field, the text is replaced by the full path of the current file, which is not the case for standard build file.

In practice, I don't think it's really an issue.
