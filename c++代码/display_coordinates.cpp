#include <windows.h>
#include <fstream>
#include <vector>
#include "json\single_include\nlohmann\json.hpp" // 需要先安装此库
#include <BaseTsd.h>

using json = nlohmann::json;

// 全局变量：存储从JSON加载的矩形坐标数据
std::vector<RECT> g_coordinates;

// 设置窗口点击穿透功能
// 参数 hwnd: 窗口句柄
void SetClickThrough(HWND hwnd) {
    // 设置窗口扩展样式（添加分层和透明属性）
    SetWindowLong(hwnd, GWL_EXSTYLE, 
        GetWindowLong(hwnd, GWL_EXSTYLE) | 
        WS_EX_LAYERED );// |     // 分层窗口
        //WS_EX_TRANSPARENT); // 允许鼠标穿透
    
    // 设置窗口透明度（255表示完全不透明，但配合WS_EX_TRANSPARENT仍可穿透）
    //SetLayeredWindowAttributes(hwnd, 100, 255, LWA_COLORKEY);
}

// 从JSON文件加载坐标数据
// 参数 path: JSON文件路径
// 返回值: 加载是否成功
bool LoadCoordinates(const std::string& path) {
    try {
        std::ifstream file(path);
        json data = json::parse(file);  // 解析JSON数据
        
        for (auto& item : data) {
            auto coords = item["坐标位置"];  // 读取坐标数组
            // 将坐标存入RECT结构体并添加到全局容器
            g_coordinates.push_back({
                coords[0], coords[1],  // left, top
                coords[2], coords[3]   // right, bottom
            });
        }
        return true;
    } catch (...) {  // 捕获所有异常（文件不存在/格式错误等）
        return false;
    }
}

// 在设备上下文绘制所有矩形框
// 参数 hdc: 设备上下文句柄
void DrawBoxes(HDC hdc) {
    HPEN hPen = CreatePen(PS_SOLID, 2, RGB(255, 0, 0)); // 创建红色实线画笔
    SelectObject(hdc, hPen);  // 选入设备上下文
    
    // 遍历所有坐标绘制矩形
    for (auto& rect : g_coordinates) {
        Rectangle(hdc, 
            rect.left, rect.top,
            rect.right, rect.bottom);
    }
    DeleteObject(hPen);  // 释放画笔资源
}

// 窗口消息处理函数
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch(msg) {
        case WM_CREATE:  // 窗口创建时
            if (!LoadCoordinates("new_output.json")) {
                MessageBox(hwnd, "JSON加载失败", "错误", MB_OK);
                ExitProcess(1);  // 加载失败则终止进程
            }
            return 0;
            
        case WM_PAINT: {  // 窗口需要重绘时
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            DrawBoxes(hdc);      // 执行绘制操作
            EndPaint(hwnd, &ps);
            return 0;
        }
        
        case WM_DESTROY:  // 窗口销毁时
            PostQuitMessage(0);  // 退出消息循环
            return 0;
    }
    return DefWindowProc(hwnd, msg, wParam, lParam);  // 默认消息处理
}

// 程序入口
int WINAPI WinMain(HINSTANCE hInst, HINSTANCE, LPSTR, int nCmdShow) {
    // 创建全屏顶层窗口（STATIC类用于简单绘制）
    HWND hwnd = CreateWindowEx(
        WS_EX_TOPMOST | WS_EX_LAYERED,  // 窗口置顶且分层
        "STATIC", NULL, WS_POPUP,       // 无边框弹出式窗口
        0, 0,                          // 位置
        GetSystemMetrics(SM_CXSCREEN),  // 宽度
        GetSystemMetrics(SM_CYSCREEN),  // 高度
        NULL, NULL, hInst, NULL);
    
    SetClickThrough(hwnd);  // 设置点击穿透
    
    // 替换窗口过程函数（原始STATIC窗口过程不支持自定义处理）
    SetWindowLongPtr(hwnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
    
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);
    
    // 消息循环
    MSG msg;
    while(GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return msg.wParam;
}