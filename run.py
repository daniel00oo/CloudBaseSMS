import Runner
import platform

r = Runner.Runner('files.json')
r.run(platform.system())