// import { Box, Slider, IconButton, Paper, Typography } from '@mui/material';
// import { useEffect, useRef, useState } from 'react';
// import ZoomInIcon from '@mui/icons-material/ZoomIn';
// import ZoomOutIcon from '@mui/icons-material/ZoomOut';
// import RestartAltIcon from '@mui/icons-material/RestartAlt';

// interface SvgRendererProps {
//   svgCode: string;
// }

// const SvgRenderer = ({ svgCode }: SvgRendererProps) => {
//   const containerRef = useRef<HTMLDivElement>(null);
//   const [zoom, setZoom] = useState<number>(100);
  
//   useEffect(() => {
//     if (containerRef.current) {
//       containerRef.current.innerHTML = svgCode;
      
//       // Apply zoom to all SVG elements
//       const svgElements = containerRef.current.querySelectorAll('svg');
//       svgElements.forEach(svg => {
//         svg.style.transform = `scale(${zoom / 100})`;
//         svg.style.transformOrigin = 'center';
//         svg.style.transition = 'transform 0.3s ease';
//       });
//     }
//   }, [svgCode, zoom]);

//   const handleZoomIn = () => {
//     setZoom(prev => Math.min(prev + 25, 300));
//   };

//   const handleZoomOut = () => {
//     setZoom(prev => Math.max(prev - 25, 25));
//   };

//   const handleReset = () => {
//     setZoom(100);
//   };

//   const handleZoomChange = (event: Event, newValue: number | number[]) => {
//     setZoom(newValue as number);
//   };

//   return (
//     <Box>
//       <Paper 
//         sx={{ 
//           p: 1, 
//           mb: 2, 
//           display: 'flex', 
//           alignItems: 'center',
//           gap: 2,
//           backgroundColor: 'background.paper'
//         }}
//       >
//         <Typography variant="body2" color="text.secondary">
//           Zoom: {zoom}%
//         </Typography>
//         <Slider
//           value={zoom}
//           onChange={handleZoomChange}
//           min={25}
//           max={300}
//           step={5}
//           sx={{ width: '200px', mx: 2 }}
//         />
//         <IconButton onClick={handleZoomOut} color="primary" size="small">
//           <ZoomOutIcon />
//         </IconButton>
//         <IconButton onClick={handleZoomIn} color="primary" size="small">
//           <ZoomInIcon />
//         </IconButton>
//         <IconButton onClick={handleReset} color="secondary" size="small">
//           <RestartAltIcon />
//         </IconButton>
//       </Paper>
      
//       <Paper
//         sx={{
//           width: '100%',
//           height: '500px',
//           border: '1px solid #e0e0e0',
//           borderRadius: 1,
//           overflow: 'auto',
//           p: 2,
//           display: 'flex',
//           justifyContent: 'center',
//           alignItems: 'center',
//           position: 'relative',
//           backgroundColor: '#FFFFFF',
//           backgroundImage: 'linear-gradient(#f1f1f1 1px, transparent 1px), linear-gradient(90deg, #f1f1f1 1px, transparent 1px)',
//           backgroundSize: '20px 20px',
//         }}
//       >
//         <Box 
//           ref={containerRef} 
//           sx={{ 
//             width: '100%',
//             height: '100%',
//             display: 'flex',
//             justifyContent: 'center',
//             alignItems: 'center',
//           }}
//         />
//       </Paper>
//     </Box>
//   );
// };

// export default SvgRenderer;









import { Box, Slider, IconButton, Paper, Typography } from '@mui/material';
import { useEffect, useRef, useState } from 'react';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import ZoomOutIcon from '@mui/icons-material/ZoomOut';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

interface SvgRendererProps {
  svgCode: string;
}

const SvgRenderer = ({ svgCode }: SvgRendererProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const svgWrapperRef = useRef<HTMLDivElement>(null);
  const [zoom, setZoom] = useState<number>(100);
  const [hasRendered, setHasRendered] = useState<boolean>(false);
  
  // Initial render of the SVG
  useEffect(() => {
    if (svgWrapperRef.current) {
      // Clear previous content and insert the new SVG
      svgWrapperRef.current.innerHTML = svgCode;
      
      // Find the SVG element and ensure it has proper dimensions
      const svgElements = svgWrapperRef.current.querySelectorAll('svg');
      svgElements.forEach(svg => {
        // Make sure the SVG has viewBox if not already set
        if (!svg.getAttribute('viewBox')) {
          // Try to get dimensions from width/height attributes
          let width = svg.getAttribute('width') ? parseFloat(svg.getAttribute('width') || '0') : 0;
          let height = svg.getAttribute('height') ? parseFloat(svg.getAttribute('height') || '0') : 0;
          
          // If no width/height attributes, try to determine from the content
          if (width === 0 || height === 0) {
            const bbox = svg.getBBox ? svg.getBBox() : { width: 800, height: 600 };
            width = bbox.width || 800;
            height = bbox.height || 600;
          }
          
          // Apply viewBox with some padding
          svg.setAttribute('viewBox', `-10 -10 ${width + 20} ${height + 20}`);
        }
        
        // Remove any fixed width/height to allow proper scaling
        svg.removeAttribute('width');
        svg.removeAttribute('height');
        
        // Make the SVG responsive while maintaining aspect ratio
        svg.style.width = '100%';
        svg.style.height = '100%';
        svg.style.maxHeight = '100%';
        svg.style.maxWidth = '100%';
        svg.style.display = 'block';
      });
      
      // After updating the SVG, ensure it's properly positioned
      // Set hasRendered to true after initial render
      setHasRendered(true);
    }
  }, [svgCode]);

  // Effect that runs once after the initial render
  useEffect(() => {
    // Set initial zoom to fit the wireframe better
    if (hasRendered && svgWrapperRef.current) {
      // Analyze the SVG to determine optimal initial zoom
      const svgElement = svgWrapperRef.current.querySelector('svg');
      if (svgElement && containerRef.current) {
        const svgWidth = svgElement.getBoundingClientRect().width;
        const containerWidth = containerRef.current.clientWidth - 40; // Account for padding
        
        if (svgWidth > 0 && containerWidth > 0) {
          // Calculate zoom to fit SVG properly (with some margin)
          const optimalZoom = Math.min(200, Math.max(80, (containerWidth / svgWidth) * 100 * 0.85));
          if (Math.abs(optimalZoom - zoom) > 10) {
            setZoom(Math.round(optimalZoom));
          }
        }
      }
    }
  }, [hasRendered]);

  // Apply zoom effect to the wrapper element separately from the SVG insertion
  useEffect(() => {
    if (svgWrapperRef.current && containerRef.current) {
      // Center the wrapper within the container
      const scaleFactor = zoom / 100;
      svgWrapperRef.current.style.transform = `scale(${scaleFactor})`;
      
      // Ensure visibility of the entire wireframe by setting an appropriate initial scroll position
      // This is especially important when the component first renders
      const container = containerRef.current;
      const wrapper = svgWrapperRef.current;
      
      // Reset scroll position to the top when zoom changes
      // This ensures the top of the wireframe is always visible
      container.scrollTop = 0;
      container.scrollLeft = 0;
    }
  }, [zoom]);

  const handleZoomIn = () => {
    setZoom(prev => Math.min(prev + 25, 300));
  };

  const handleZoomOut = () => {
    setZoom(prev => Math.max(prev - 25, 25));
  };

  const handleReset = () => {
    setZoom(100);
  };

  const handleZoomChange = (event: Event, newValue: number | number[]) => {
    setZoom(newValue as number);
  };

  return (
    <Box>
      <Paper 
        sx={{ 
          p: 1, 
          mb: 2, 
          display: 'flex', 
          alignItems: 'center',
          gap: 2,
          backgroundColor: 'background.paper'
        }}
      >
        <Typography variant="body2" color="text.secondary">
          Zoom: {zoom}%
        </Typography>
        <Slider
          value={zoom}
          onChange={handleZoomChange}
          min={25}
          max={300}
          step={5}
          sx={{ width: '200px', mx: 2 }}
        />
        <IconButton onClick={handleZoomOut} color="primary" size="small">
          <ZoomOutIcon />
        </IconButton>
        <IconButton onClick={handleZoomIn} color="primary" size="small">
          <ZoomInIcon />
        </IconButton>
        <IconButton onClick={handleReset} color="secondary" size="small">
          <RestartAltIcon />
        </IconButton>
      </Paper>
      
      <Paper
        ref={containerRef}
        sx={{
          width: '100%',
          height: '600px', // Increased height for better visibility
          border: '1px solid #e0e0e0',
          borderRadius: 1,
          overflow: 'auto',
          p: 2,
          position: 'relative',
          backgroundColor: '#FFFFFF',
          backgroundImage: 'linear-gradient(#f1f1f1 1px, transparent 1px), linear-gradient(90deg, #f1f1f1 1px, transparent 1px)',
          backgroundSize: '20px 20px',
        }}
      >
        <Box 
          sx={{
            width: '100%',
            height: '100%',
            display: 'flex',
            justifyContent: 'flex-start',
            alignItems: 'flex-start',
            overflow: 'visible'
          }}
        >
          <Box
            ref={svgWrapperRef}
            sx={{ 
              transformOrigin: 'top left',
              transition: 'transform 0.3s ease',
              width: 'auto',
              height: 'auto',
              display: 'flex',
              justifyContent: 'flex-start',
              alignItems: 'flex-start',
              margin: '10px',
              paddingTop: '20px'
            }}
          />
        </Box>
      </Paper>
    </Box>
  );
};

export default SvgRenderer;




// import { Box } from '@mui/material';
// import { useEffect, useRef } from 'react';

// interface SvgRendererProps {
//   svgCode: string;
// }

// const SvgRenderer = ({ svgCode }: SvgRendererProps) => {
//   const containerRef = useRef<HTMLDivElement>(null);

//   useEffect(() => {
//     if (containerRef.current) {
//       containerRef.current.innerHTML = svgCode;
//     }
//   }, [svgCode]);

//   return (
//     <Box 
//       ref={containerRef} 
//       sx={{ 
//         width: '100%', 
//         height: '400px',
//         border: '1px dashed #ccc',
//         borderRadius: 1,
//         overflow: 'auto',
//         p: 2,
//         display: 'flex',
//         justifyContent: 'center',
//         '& svg': {
//           maxWidth: '100%',
//           maxHeight: '100%',
//         }
//       }}
//     />
//   );
// };

// export default SvgRenderer;