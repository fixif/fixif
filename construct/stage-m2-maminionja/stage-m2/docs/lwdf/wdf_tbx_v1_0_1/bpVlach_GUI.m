function varargout = bpVlach_GUI(varargin)
% BPVLACH_GUI M-file for bpVlach_GUI.fig
%      BPVLACH_GUI, by itself, creates a new BPVLACH_GUI or raises the existing
%      singleton*.
%
%      H = BPVLACH_GUI returns the handle to a new BPVLACH_GUI or the handle to
%      the existing singleton*.
%
%      BPVLACH_GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in BPVLACH_GUI.M with the given input arguments.
%
%      BPVLACH_GUI('Property','Value',...) creates a new BPVLACH_GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before bpVlach_GUI_OpeningFunction gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to bpVlach_GUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help bpVlach_GUI

% Last Modified by GUIDE v2.5 05-Mar-2004 20:56:15

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @bpVlach_GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @bpVlach_GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin & isstr(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before bpVlach_GUI is made visible.
function bpVlach_GUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to bpVlach_GUI (see VARARGIN)

% Choose default command line output for bpVlach_GUI
handles.output = hObject;

% Update handles structure
handles.sDomain            =     1;
set( handles.radiobutton_sDomain,     'Value', 1 );
handles.freqNormMode       =     1;
set( handles.radiobutton_freqMode1,   'Value', 1 );
handles.filterOrder        =    [];
set( handles.radiobutton_freqMode1,   'Value', 1 );

handles.fcLow			   =    [];
handles.fcHigh			   =    [];
handles.nZerosInFreq0	   =     1;
set( handles.edit_nZerosInFreq0,     'String', '1' );
handles.lowerBandZeroFreqs =    [];
handles.upperBandZeroFreqs =    [];
handles.stopBandZeros      =     1;
handles.figHsShown         =     0;
handles.figHzShown         =     0;
handles.figsLWDFShown      =     0;
% Update handles structure
guidata(hObject, handles);

% use a .png file for the logo with a transparant background ...
TUD_logo = 'TUD_bl-zw.png';
set(hObject, 'Units', 'pixels' );
% ... and let this machine's set-up fill in the background
handles.logo1 = imread( TUD_logo,'BackgroundColor', get(hObject,'Color') );
axes(handles.axes1);
image(handles.logo1);
set(handles.axes1, 'Visible', 'off', 'Units', 'pixels' );

% UIWAIT makes bpVlach_GUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = bpVlach_GUI_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;




% --- Executes on button press in radiobutton_sDomain.
function radiobutton_sDomain_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_sDomain, 'Value' ) == 0 )
		set( handles.radiobutton_sDomain, 'Value', 1 );
	else
		set( handles.radiobutton_zDomain, 'Value', 0 );
		handles.sDomain = 1;
		%---
		handles.fcLow  = lfSwitchDomain( handles.fcLow, 's' );
		set( handles.edit_fcLow, 'String', lfFormattedString(handles.fcLow) );
		%---
		handles.fcHigh  = lfSwitchDomain( handles.fcHigh, 's' );
		set( handles.edit_fcHigh, 'String', lfFormattedString(handles.fcHigh) );
		%---
		handles.lowerBandZeroFreqs   = lfSwitchDomain( handles.lowerBandZeroFreqs, 's' );
		set( handles.edit_lowerBandZeroFreqs, 'String', ...
										lfFormattedString( handles.lowerBandZeroFreqs ) );
		%---
		handles.upperBandZeroFreqs   = lfSwitchDomain( handles.upperBandZeroFreqs, 's' );
		set( handles.edit_upperBandZeroFreqs, 'String', ...
										lfFormattedString( handles.upperBandZeroFreqs ) );
	end
	guidata( hObject, handles );			% store the changes


% --- Executes on button press in radiobutton_zDomain.
function radiobutton_zDomain_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_zDomain, 'Value' ) == 0 )
		set( handles.radiobutton_zDomain, 'Value', 1 );
	else
		set( handles.radiobutton_sDomain, 'Value', 0 );
		handles.sDomain = 0;
		%---
		handles.fcLow  = lfSwitchDomain( handles.fcLow, 'z' );
		set( handles.edit_fcLow, 'String', lfFormattedString(handles.fcLow) );
		%---
		handles.fcHigh  = lfSwitchDomain( handles.fcHigh, 'z' );
		set( handles.edit_fcHigh, 'String', lfFormattedString(handles.fcHigh) );
		%---
		handles.lowerBandZeroFreqs   = lfSwitchDomain( handles.lowerBandZeroFreqs, 'z' );
		set( handles.edit_lowerBandZeroFreqs, 'String', ...
										lfFormattedString( handles.lowerBandZeroFreqs ) );
		%---
		handles.upperBandZeroFreqs   = lfSwitchDomain( handles.upperBandZeroFreqs, 'z' );
		set( handles.edit_upperBandZeroFreqs, 'String', ...
										lfFormattedString( handles.upperBandZeroFreqs ) );
	end
	guidata( hObject, handles );			% store the changes


% --- Executes on button press in radiobutton_freqMode1.
function radiobutton_freqMode1_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_freqMode1, 'Value' ) == 0 )
		set( handles.radiobutton_freqMode1, 'Value', 1 );
	else
		set( handles.radiobutton_freqMode0, 'Value', 0 );
		handles.freqNormMode = 1;
	end
	guidata( hObject, handles );			% store the changes


% --- Executes on button press in radiobutton_freqMode0.
function radiobutton_freqMode0_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_freqMode0, 'Value' ) == 0 )
		set( handles.radiobutton_freqMode0, 'Value', 1 );
	else
		set( handles.radiobutton_freqMode1, 'Value', 0 );
		handles.freqNormMode = 0;
	end
	guidata( hObject, handles );			% store the changes



% --- Executes during object creation, after setting all properties.
function edit_filterOrder_CreateFcn(hObject, eventdata, handles)
if ispc
    set(hObject,'BackgroundColor','white');
else
    set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
end

function edit_filterOrder_Callback(hObject, eventdata, handles)
	prevValue = handles.filterOrder;
	filterOrder = round( str2double( get( hObject, 'String' ) ) );
	valid = ( (filterOrder >= 2) & (rem(filterOrder,2) == 0) );
	if valid
		nStopBandZeros = length( handles.stopBandZeros );
		nPossibleStopBandZeros = floor( filterOrder / 2 );
		if ( nStopBandZeros > nPossibleStopBandZeros )
			errordlg( 'Too many stopband zeros for this filterorder ...', ...
								'FilterOrder vs stopBandZeros mismatch', 'modal' );
			valid = 0;
		end
	else
		errordlg( 'Positive EVEN filterorders expected ...', 'FilterOrder Error', 'modal' );
	end
	if ~valid
		beep;
		filterOrder = prevValue;
	end
	handles.filterOrder = filterOrder;
	guidata( hObject, handles );			% store the changes
	set( hObject, 'String', int2str(filterOrder) );



% --- Executes during object creation, after setting all properties.
function edit_passBandRipple_dB_CreateFcn(hObject, eventdata, handles)
if ispc
    set(hObject,'BackgroundColor','white');
else
    set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
end

function edit_passBandRipple_dB_Callback(hObject, eventdata, handles)
	handles.passBandRipple_dB = abs( str2num(get( hObject, 'String')) );
	set( hObject, 'String', num2str(handles.passBandRipple_dB) );
	guidata( hObject, handles );			% store the changes



% --- Executes during object creation, after setting all properties.
function edit_fcLow_CreateFcn(hObject, eventdata, handles)
  if ispc
      set(hObject,'BackgroundColor','white');
  else
      set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
  end

function edit_fcLow_Callback(hObject, eventdata, handles)
	newValue = str2double(get( hObject, 'String'));
	if ( ( handles.sDomain == 0 )  & ~( ( newValue >= 0.0 ) & ( newValue < 0.5 ) ) )
		errordlg( 'z-domain frequencies should be between 0.0 and 0.5 ...', ...
		                                                   'Input Out of Range', 'modal' );
		beep;
	else
		handles.fcLow = newValue;
	end
	set( handles.edit_fcLow, 'String', lfFormattedString(handles.fcLow) );
	guidata( hObject, handles );			% store the changes if any



% --- Executes during object creation, after setting all properties.
function edit_fcHigh_CreateFcn(hObject, eventdata, handles)
  if ispc
      set(hObject,'BackgroundColor','white');
  else
      set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
  end

function edit_fcHigh_Callback(hObject, eventdata, handles)
	newValue = str2double(get( hObject, 'String'));
	if ( ( handles.sDomain == 0 )  & ~( ( newValue >= 0.0 ) & ( newValue < 0.5 ) ) )
		errordlg( 'z-domain frequencies should be between 0.0 and 0.5 ...', ...
		                                                   'Input Out of Range', 'modal' );
		beep;
	else
		handles.fcHigh = newValue;
	end
	set( handles.edit_fcHigh, 'String', lfFormattedString(handles.fcHigh) );
	guidata( hObject, handles );			% store the changes if any


% --- Executes during object creation, after setting all properties.
function edit_nZerosInFreq0_CreateFcn(hObject, eventdata, handles)
  if ispc
      set(hObject,'BackgroundColor','white');
  else
      set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
  end

function edit_nZerosInFreq0_Callback(hObject, eventdata, handles)
	% use str2num, because string can be empty
	newValue = round( abs( str2num( get( hObject, 'String' ) ) ) );
	if ( isempty(newValue) | (rem(newValue,2) == 0) )
		errordlg( 'This should be an ODD number of single zeros ...', ...
	                                                   'Single Zeros Error', 'modal' );
		beep;
	else
		handles.nZerosInFreq0 = newValue;
	end
	set( handles.edit_nZerosInFreq0, 'String', int2str(handles.nZerosInFreq0) );
	guidata( hObject, handles );			% store the changes


% --- Executes during object creation, after setting all properties.
function edit_lowerBandZeroFreqs_CreateFcn(hObject, eventdata, handles)
  if ispc
      set(hObject,'BackgroundColor','white');
  else
      set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
  end

function edit_lowerBandZeroFreqs_Callback(hObject, eventdata, handles)
	newValue = str2num(get( hObject, 'String'));
	if ( ( handles.sDomain == 0 )  & ~( all( newValue >= 0.0 ) & all( newValue < 0.5 ) ) )
		errordlg( 'All z-domain frequencies should be between 0.0 and 0.5 ...', ...
		                                                   'Input Out of Range', 'modal' );
		beep;
	else	                                                  
		handles.lowerBandZeroFreqs = newValue;
		guidata( hObject, handles );			% store the changes
	end
	set( handles.edit_lowerBandZeroFreqs, 'String', ...
										lfFormattedString( handles.lowerBandZeroFreqs ) );



% --- Executes during object creation, after setting all properties.
function edit_upperBandZeroFreqs_CreateFcn(hObject, eventdata, handles)
  if ispc
      set(hObject,'BackgroundColor','white');
  else
      set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
  end

function edit_upperBandZeroFreqs_Callback(hObject, eventdata, handles)
	newValue = str2num(get( hObject, 'String'));
	if ( ( handles.sDomain == 0 )  & ~( all( newValue >= 0.0 ) & all( newValue < 0.5 ) ) )
		errordlg( 'All z-domain frequencies should be between 0.0 and 0.5 ...', ...
		                                                   'Input Out of Range', 'modal' );
		beep;
	else	                                                  
		handles.upperBandZeroFreqs = newValue;
		guidata( hObject, handles );			% store the changes
	end
	set( handles.edit_upperBandZeroFreqs, 'String', ...
										lfFormattedString( handles.upperBandZeroFreqs ) );



% --- Executes on button press in checkbox_plotHs.
function checkbox_plotHs_Callback(hObject, eventdata, handles)

% --- Executes on button press in checkbox_plotHz.
function checkbox_plotHz_Callback(hObject, eventdata, handles)

% --- Executes on button press in checkbox_LWDF.
function checkbox_LWDF_Callback(hObject, eventdata, handles)


% --- Executes on button press in pushbutton_Apply.
function pushbutton_Apply_Callback(hObject, eventdata, handles)

	% first check that all necassary parameters are specified
	result = 1;
	conflictingParameters = 0;
	filterOrder  = handles.filterOrder;
	sDomain      = handles.sDomain;
	if isempty( filterOrder )
		errordlg( 'Should specify at least a filter Order ...', 'Missing Input', 'modal' );
		conflictingParameters = 1;
	else
		passBandRipple_dB  = handles.passBandRipple_dB;
		freqNormMode       = handles.freqNormMode;
		cutOffFrequencies  = [ handles.fcLow  handles.fcHigh ];
		lowerBandZeroFreqs = handles.lowerBandZeroFreqs;
		upperBandZeroFreqs = handles.upperBandZeroFreqs;
		stopBandZeros   = [ zeros(1,handles.nZerosInFreq0)  lowerBandZeroFreqs ...
										                     		  upperBandZeroFreqs ]; 
		if isempty( passBandRipple_dB )
			errordlg( 'Should specify a passband ripple ...', 'Missing Input', 'modal' );
			conflictingParameters = 1;
		elseif ( max(lowerBandZeroFreqs) >= cutOffFrequencies(1) )
			errordlg( 'Lower band zero frequencies not all below lower cut-off frequency ...', ...
														'Parameter''s Mismatch', 'modal' );
			conflictingParameters = 1;
		elseif ( min(upperBandZeroFreqs) <= cutOffFrequencies(2) )
			errordlg( 'Upper band zero frequencies not all above upper cut-off frequency ...', ...
														'Parameter''s Mismatch', 'modal' );
			conflictingParameters = 1;
		elseif ( length(stopBandZeros) > filterOrder/2 )
			errordlg( 'Too many stopband zeros for given filterorder ...', ...
														'Parameter''s Mismatch', 'modal' );
			conflictingParameters = 1;
		end

	end
	if ~conflictingParameters
		if ( sDomain == 0 )
			stopBandZeros     = lfSwitchDomain( stopBandZeros, 's' );
			cutOffFrequencies = lfSwitchDomain( cutOffFrequencies, 's' );
		end
%		nUnitElements = handles.nUnitElements;
		nUnitElements = 0;
		Hs = Hs_bpVlach( filterOrder, passBandRipple_dB, cutOffFrequencies, ...
									stopBandZeros, nUnitElements, freqNormMode );

%====
		if ( get( handles.checkbox_plotHs, 'Value' ) == 1 )
			plotHs( Hs, 1, 1 );
			handles.figHsShown = 1;
			assignin( 'base', 'Hs_GUI', Hs );
		elseif ( handles.figHsShown ~= 0 )
			close( figure(1) );
			handles.figHsShown = 0;
		end
%====
		if ( get( handles.checkbox_plotHz, 'Value' ) == 1 )
			Hz = Hs2Hz( Hs );
			plotHz( Hz, 1, 2 );
			handles.figHzShown = 1;
			assignin( 'base', 'Hz_GUI', Hz );
		elseif ( handles.figHzShown ~= 0 )
			close( figure(2) );
			handles.figHzShown = 0;
		end
%====
		if ( (result == 1) & ( get( handles.checkbox_LWDF, 'Value' ) == 1 ) )
		% be sure to pass always only one Hs (bireciprocal cauer !) 
			[LWDF,Hz_LWDF,Messages] = Hs2LWDF( Hs(1), 0, 0 );	
			if isempty(Messages.error)
				fprintf( Messages.warning );
				showLWDF( LWDF, 'L', 3 );
				plotHz( Hz_LWDF, 1,4, 0,2000, ...
							'Transfer Function reconstructed from LWDF Coefficients', ...
											[ ' forward B_{fwd}'; ' reverse B_{rev}' ] );
				axis( [ xlim -80 10 ] );											
				handles.figsLWDFShown = 1;
				assignin( 'base', 'LWDF_GUI', LWDF );
			else
				errordlg( Messages.error, 'LWDF Constraints Error', 'modal' );
				beep;
			end			
		elseif ( handles.figsLWDFShown ~= 0 )
			close( figure(3) );
			close( figure(4) );
			handles.figsLWDFShown = 0;
		end
		
		fprintf( '\n\n=====================================================\n\n' );

	else	% there are conflictingParameters
		beep;
	end		% test on conflictingParameters
	guidata( hObject, handles );		% update figShown handles



% --- Executes on button press in pushbutton_Quit.
function pushbutton_Quit_Callback(hObject, eventdata, handles)
	% Get the current position of the GUI from the handles structure
	% to pass to the modal dialog.
	pos_size = get(handles.figure1, 'Position' );
	% Call modaldlg with the argument 'Position'
	userResponse = modaldlg('Title','Confirm Quit');
	if strcmp( userResponse,'Yes' )
		delete(handles.figure1);
	end
	



%==========================================================================================
%=========  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ============
%==========================================================================================

function freq2 = lfSwitchDomain(freq1,newDomain)
  % Bilinear or Inverse bilinear frequency translation 
  %	fz = 0.25 corresponds with fs = 1.0
  if ( newDomain == 'z' )
	  freq2 = atan(freq1) / pi;
  else		% newDomain == 's'
	  freq2 = tan(freq1*pi);
  end

	
%==========================================================================================
function formattedStr = lfFormattedString(showValues);
	nValues = length( showValues );
	tmpStr  = [];
	for i = 1:nValues
		addStr = num2str( abs(showValues(i)), 5 );
		if isempty( find(addStr == '.') )
			addStr = [ addStr '.0' ];
		end
		if ( i ~= nValues )
			addStr = [ addStr '  ' ];
		end
		tmpStr = [ tmpStr addStr ];
	end
	formattedStr = tmpStr;	




