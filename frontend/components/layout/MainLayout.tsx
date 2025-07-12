import React from 'react';
import { Box, AppBar, Toolbar, Typography, Button, Drawer, List, ListItem, ListItemText } from '@mui/material';
import { useRouter } from 'next/router';

const navigationItems = [
  { path: '/', label: 'Home' },
  { path: '/dashboard', label: 'Dashboard' },
  { path: '/configure-env', label: 'Configure Environment' },
  { path: '/improvement', label: 'Improvement' },
  { path: '/pricing', label: 'Pricing' },
  { path: '/about', label: 'About' },
  { path: '/contact', label: 'Contact' },
];

const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const router = useRouter();

  return (
    <Box sx={{ display: 'flex' }}>
      {/* Sidebar */}
      <Drawer
        variant="permanent"
        sx={{
          width: 240,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 240,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <List>
          {navigationItems.map((item) => (
            <ListItem
              button
              key={item.path}
              onClick={() => router.push(item.path)}
              selected={router.pathname === item.path}
            >
              <ListItemText primary={item.label} />
            </ListItem>
          ))}
        </List>
      </Drawer>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - 240px)` },
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default MainLayout;
