import os

# Fix for OMP: Error #15 (clash between torch and system OpenMP)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys

# EARLY GPU ISOLATION: Must be done before importing torch
if "--gpu_id" in sys.argv:
    try:
        idx = sys.argv.index("--gpu_id") + 1
        if idx < len(sys.argv):
            gid = sys.argv[idx]
            os.environ["CUDA_VISIBLE_DEVICES"] = str(gid)
            print(f"--> [SYSTEM] Enforcing isolation: CUDA_VISIBLE_DEVICES={gid}")
    except ValueError:
        pass

import argparse
import time
import platform
import torch

# Force UTF-8 for progress bars
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import rasterio
from rasterio.plot import reshape_as_image
from rasterio.crs import CRS
import easyocr
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np

# Rich imports for the Minimalist Vibrant UI
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, MofNCompleteColumn, TaskProgressColumn
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

# Custom vibrant theme
vibrant_theme = Theme({
    "info": "bold cyan",
    "success": "bold bright_green",
    "warning": "bold yellow",
    "error": "bold red",
    "vibrant": "bold magenta",
    "highlight": "bold dodger_blue1",
})

console = Console(theme=vibrant_theme)

def get_hardware_str(use_gpu, gpu_id):
    if use_gpu and torch.cuda.is_available():
        # When CUDA_VISIBLE_DEVICES is set, the visible device is always index 0
        name = torch.cuda.get_device_name(0)
        return f"[bold bright_green]GPU ACCELERATED[/] [dim]({name} | ID:{gpu_id})[/]"
    return "[bold yellow]CPU ENGINE[/] [dim](Standard performance)[/]"

def extract_map_text(input_tif, output_shp, proj_path=None, confidence=40, use_gpu=False, gpu_id=0):
    # Hardware Check
    is_cuda = torch.cuda.is_available()
    if use_gpu and not is_cuda:
        console.print("\n[warning]![/] [bold yellow]Neural Engine Warning:[/] CUDA not detected. Reverting to standard CPU processing.\n")
        use_gpu = False

    hw_status = get_hardware_str(use_gpu, gpu_id)
    
    # 1. SHOWCASE HEADER WITH AI BRANDING
    ai_badge = "[black on bright_magenta] AI [/]"
    header_title = f"{ai_badge} [vibrant]NEURAL TEXT DISCOVERY[/]"
    
    console.print(f"\n{header_title}")
    console.print(f"[highlight]PROJECT CORE:[/] [white]Vision Intelligence Unit v2.5[/]")
    console.print(f"[highlight]WRITTEN BY:[/] [white]MUKTIKANTA OJHA 😎[/]")
    console.print(f"[highlight]TARGET DATA:[/] [white]{os.path.basename(input_tif)}[/]")
    console.print(f"[highlight]HARDWARE:   [/] {hw_status}\n")

    # 2. RUN AI SCAN
    try:
        with console.status("[vibrant]Initializing Neural Core...[/]", spinner="dots12") as status:
            if use_gpu: 
                # With strict isolation, we always reference the first visible device (0)
                torch.cuda.set_device(0)
            
            # EasyOCR should automatically pick up the visible device
            reader = easyocr.Reader(['en'], gpu=use_gpu)
            
            status.update("[vibrant]Deconstructing Raster Density...[/]")
            with rasterio.open(input_tif) as src:
                raster_data = src.read()
                transform = src.transform
                native_crs = src.crs
                image_array = reshape_as_image(raster_data)
                if raster_data.dtype != 'uint8':
                    image_array = (image_array / image_array.max() * 255).astype('uint8')
                if len(image_array.shape) == 3 and image_array.shape[2] == 4:
                    image_array = image_array[:, :, :3]
            
            final_crs = native_crs
            if proj_path:
                if proj_path.lower().endswith('.prj'):
                    with open(proj_path, 'r') as f:
                        final_crs = CRS.from_wkt(f.read())
                else:
                    with rasterio.open(proj_path) as src:
                        final_crs = src.crs

            status.update("[vibrant]Streaming Vision Frequencies...[/]")
            results = reader.readtext(image_array, detail=1, paragraph=False)
            
    except Exception as e:
        console.print(f"\n[error]ENGINE COLLAPSE:[/] {e}")
        sys.exit(1)

    # 3. EXTRACTION FEED & PREMIUM 3D PROGRESS BAR
    geometries = []
    texts = []
    found_count = 0
    
    console.print(f"[success]Analysis complete.[/] [dim]Processing {len(results)} potential signatures...[/]\n")

    # Premium 3D-styled progress bar
    progress = Progress(
        SpinnerColumn(spinner_name="simpleDotsScrolling"),
        TextColumn("[highlight]{task.description}"),
        BarColumn(
            bar_width=None, 
            style="grey15", 
            complete_style="bold dodger_blue1", 
            finished_style="bold spring_green3"
        ),
        MofNCompleteColumn(),
        TaskProgressColumn(text_format="[bold cyan]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        expand=True
    )

    with Live(progress, refresh_per_second=20, transient=False):
        task = progress.add_task("SYNTHESIZING DATA...", total=len(results))
        
        for (bbox, text, conf) in results:
            progress.update(task, advance=1)
            conf_int = int(conf * 100)
            
            if conf_int >= confidence:
                xs = [p[0] for p in bbox]
                ys = [p[1] for p in bbox]
                gx, gy = transform * (sum(xs)/4.0, sum(ys)/4.0)
                
                geometries.append(Point(gx, gy))
                texts.append(text)
                found_count += 1
                
                # Stylish premium print
                color = "bright_green" if conf_int > 85 else "dodger_blue1" if conf_int > 70 else "yellow"
                mark = "◈" if conf_int > 85 else "◇"
                console.print(f" [dim]{mark}[/] [bold {color}]{text:.<34}[/] [dim]{conf_int}%[/]")
                time.sleep(0.002) # Faster for showcase performance feel

    # 4. EXPORT
    if geometries:
        with console.status("[vibrant]Committing to Spatial Lattice...[/]"):
            df = pd.DataFrame({'values': texts})
            gdf = gpd.GeoDataFrame(df, geometry=geometries, crs=final_crs)
            out_dir = os.path.dirname(output_shp)
            if out_dir and not os.path.exists(out_dir): os.makedirs(out_dir)
            gdf.to_file(output_shp, driver='ESRI Shapefile', encoding='utf-8')
        
        console.print(f"\n[success]✔ PROJECT OUTPUT READY:[/] [bold]{found_count}[/] neural signatures archived.\n")
    else:
        console.print("\n[error]![/] No significant patterns detected above threshold.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Neural extraction unit")
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--projection", "-p")
    parser.add_argument("--confidence", "-c", type=int, default=40)
    parser.add_argument("--gpu_id", type=int, default=0)

    args = parser.parse_args()
    
    # Auto-enable GPU if CUDA is present or id is specified
    use_gpu = ("--gpu_id" in sys.argv) or torch.cuda.is_available()

    if os.path.exists(args.input):
        extract_map_text(args.input, args.output, args.projection, args.confidence, use_gpu, args.gpu_id)
    else:
        console.print(f"[error]Error:[/] Target missing: {args.input}")