#测试环境apiserver地址

# 将apiserver端口暴露出来：

# 1、获取apiserver deployment的名称。
# kubectl get deployment -n kubesphere-system

# 2、修改apiserver deployment的配置文件中的hostPort
# kubectl edit deployment deployment-name -n kubesphere-system

url = 'http://139.198.9.112:9090'
