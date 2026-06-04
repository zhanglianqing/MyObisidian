```dataview
TASK
WHERE !completed AND !contains(file.path, "copilot")
GROUP BY file.link
```
