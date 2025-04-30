#include <windows.h>
#include <string>
#include <vector>
#include <algorithm> // 添加algorithm头文件

using namespace std;

struct WindowConfig {
    int x;
    int y;
    int width;
    int height;
};

vector<WindowConfig> ReadJSONConfig(const wchar_t* filename) {
    vector<WindowConfig> configs;
    HANDLE hFile = CreateFileW(filename, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if(hFile == INVALID_HANDLE_VALUE) return configs;
    
    const DWORD BUFFER_SIZE = 4096;
    char buffer[BUFFER_SIZE];
    DWORD bytesRead;
    string jsonContent;
    while(ReadFile(hFile, buffer, BUFFER_SIZE, &bytesRead, NULL) && bytesRead > 0) {
        jsonContent.append(buffer, bytesRead);
    }
    CloseHandle(hFile);
    
    size_t pos = 0;
    while((pos = jsonContent.find("坐标位置", pos)) != string::npos) {
        size_t start = jsonContent.find('[', pos);
        size_t end = jsonContent.find(']', start);
        if (start != string::npos && end != string::npos) {
            WindowConfig cfg;
            string arr = jsonContent.substr(start, end - start + 1);
            if(sscanf_s(arr.c_str(), "[%d,%d,%d,%d]", &cfg.x, &cfg.y, &cfg.width, &cfg.height) == 4) {
                cfg.width = abs(cfg.width - cfg.x);
                cfg.height = abs(cfg.height - cfg.y);
                configs.push_back(cfg);
            }
            pos = end;
        }
    }
    return configs;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_PAINT: {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);
        RECT rect;
        GetClientRect(hwnd, &rect);
        HBRUSH hBrush = CreateSolidBrush(RGB(0, 0, 0));
        FillRect(hdc, &rect, hBrush);
        DeleteObject(hBrush);
        EndPaint(hwnd, &ps);
        return 0;
    }
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    default:
        return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow) {
    auto configs = ReadJSONConfig(L"C:\\Users\\chauncyfxm\\Desktop\\Qwen2.5-VL\\new_output.json");
    
    WNDCLASSW wc = { };
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"RectWindow";
    wc.hbrBackground = NULL; // 必须设为NULL才能支持分层窗口
    RegisterClassW(&wc);
    

    vector<HWND> windows;
    int screenWidth = GetSystemMetrics(SM_CXSCREEN);
    int screenHeight = GetSystemMetrics(SM_CYSCREEN);

    for (auto& cfg : configs) {
        // 限制窗口在屏幕范围内
        cfg.width = std::min(cfg.width, screenWidth - cfg.x);
        cfg.height = std::min(cfg.height, screenHeight - cfg.y);
        // 确保窗口尺寸至少为1x1像素
        cfg.width = max(cfg.width, 1);
        cfg.height = max(cfg.height, 1);
        // 确保窗口坐标在屏幕范围内
        cfg.x = max(cfg.x, 0);
        cfg.y = max(cfg.y, 0);
        cfg.width = min(cfg.width, screenWidth - cfg.x);
        cfg.height = min(cfg.height, screenHeight - cfg.y);
        
        HWND hwnd = CreateWindowExW(
            WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_TRANSPARENT,
            L"RectWindow",
            L"Object Window",
            WS_POPUP | WS_VISIBLE,
            cfg.x,
            cfg.y,
            cfg.width,
            cfg.height,
            NULL, NULL, hInstance, NULL);
        
        if (hwnd) {
            // 设置窗口透明度（50 = 20%不透明）
            SetLayeredWindowAttributes(hwnd, 0, 50, LWA_ALPHA);
            ShowWindow(hwnd, nCmdShow);
            windows.push_back(hwnd);
        }
    }

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}