import win32gui
import win32con
import numpy as np
import ctypes
from ctypes import c_void_p

# 加载 DirectX SDK 中的 D3D10 库
d3d10 = ctypes.windll.d3d10

# 初始化 Direct3D
hwnd = 4854766  # 替换成需要截图的窗口标题
if not hwnd:
    print("未找到窗口。")
else:
    window_rect = win32gui.GetWindowRect(hwnd)
    width = window_rect[2] - window_rect[0]
    height = window_rect[3] - window_rect[1]

    dxgi_factory = ctypes.POINTER(ctypes.c_void)()
    d3d10.CreateDXGIFactory(ctypes.byref(ctypes.c_void_p(dxgi_factory)))

    device = ctypes.POINTER(ctypes.c_void)()
    swap_chain = ctypes.POINTER(ctypes.c_void)()
    adapter = ctypes.POINTER(ctypes.c_void)()
    dxgi_factory.EnumAdapters(0, ctypes.byref(adapter))
    d3d10.D3D10CreateDevice(ctypes.byref(adapter), 3, 0, 0, 0, 0, 3, ctypes.byref(device))

    swap_chain_desc = np.zeros(80, dtype=np.uint8)
    swap_chain_desc_viewport = np.zeros(24, dtype=np.uint32)
    ctypes.memset(swap_chain_desc.ctypes.data, 0, 80)
    swap_chain_desc['BufferDesc']['Width'] = width
    swap_chain_desc['BufferDesc']['Height'] = height
    swap_chain_desc['BufferDesc']['Format'] = 28  # DXGI_FORMAT_R8G8B8A8_UNORM
    swap_chain_desc['SampleDesc']['Count'] = 1
    swap_chain_desc['SampleDesc']['Quality'] = 0
    swap_chain_desc['Usage'] = 0x20  # DXGI_USAGE_RENDER_TARGET_OUTPUT
    swap_chain_desc['OutputWindow'] = hwnd
    swap_chain_desc['BufferCount'] = 1
    swap_chain_desc['SwapEffect'] = 1  # DXGI_SWAP_EFFECT_DISCARD
    swap_chain_desc['Flags'] = 0

    d3d10.DXGI_SWAP_CHAIN_DESC.restype = None
    d3d10.DXGI_SWAP_CHAIN_DESC.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint32)]
    d3d10.DXGI_SWAP_CHAIN_DESC(swap_chain_desc.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), swap_chain_desc_viewport.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)))

    dxgi_factory.CreateSwapChain(device, ctypes.byref(swap_chain_desc), ctypes.byref(swap_chain))

    back_buffer = ctypes.POINTER(ctypes.c_void)()
    texture2d_desc = ctypes.c_void_p()

    swap_chain.GetBuffer(0, ctypes.byref(ctypes.c_void_p(back_buffer)))

    back_buffer.QueryInterface(ctypes.byref(ctypes.c_void_p(d3d10.ID3D10Texture2D)), ctypes.byref(texture2d_desc))

    texture2d = ctypes.POINTER(ctypes.c_void)()
    d3d10.D3D10CreateTexture2D(device, ctypes.byref(texture2d_desc), ctypes.byref(ctypes.c_void_p(None)), ctypes.byref(texture2d))

    d3d10.ID3D10Device.CopyResource(device, ctypes.byref(texture2d), back_buffer)

    sub_resource_index = 0
    map_type = 2  # D3D10_MAP_READ
    map_flags = 0
    mapped_resource = ctypes.c_void_p()
    d3d10.ID3D10Device.Map.restype = ctypes.c_uint  # 返回值为 HRESULT
    d3d10.ID3D10Device.Map.argtypes = [ctypes.POINTER(ctypes.c_void), ctypes.c_uint, ctypes.c_uint,
                                       ctypes.c_uint, ctypes.POINTER(ctypes.c_void_p)]
    result = d3d10.ID3D10Device.Map(device, ctypes.byref(texture2d), sub_resource_index, map_type, map_flags, ctypes.byref(mapped_resource))
    if result == 0:  # S_OK
        mip_level_desc = ctypes.c_void_p()
        texture2d.QueryInterface(ctypes.byref(ctypes.c_void_p(d3d10.ID3D10Texture2D)), ctypes.byref(mip_level_desc))
        struct_size = ctypes.sizeof(d3d10.D3D10_MAPPED_TEXTURE2D)
        mapped_texture_data = np.zeros(struct_size, dtype=np.uint8)
        d3d10.D3D10_MAPPED_TEXTURE2D.restype = None
        d3d10.D3D10_MAPPED_TEXTURE2D.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_uint,
                                                 ctypes.c_uint, ctypes.POINTER(ctypes.c_void)]
        d3d10.D3D10_MAPPED_TEXTURE2D(
            ctypes.byref(mapped_resource), sub_resource_index, map_type, ctypes.byref(mapped_texture_data))
        image_data = np.frombuffer(mapped_texture_data['pData'].tobytes(), dtype=np.uint8)
        image_data = image_data.reshape((height, width, 4))  # RGBA 格式
    else:
        image_data = None

    d3d10.ID3D10Device.Unmap(device, ctypes.byref(texture2d), sub_resource_index)

    mapped_resource.Release()
    mip_level_desc.Release()
    texture2d.Release()

    back_buffer.Release()
    swap_chain.Release()
    device.Release()
    adapter.Release()
    dxgi_factory.Release()

    # 保存截图
    if image_data is not None:
        from PIL import Image
        image = Image.fromarray(image_data, mode='RGBA')
        image.save("screenshot.png")